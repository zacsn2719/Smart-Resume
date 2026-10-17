import io
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import engine, get_db, SessionLocal
from ai_service import (
    load_skills,
    extract_skills,
    extract_education,
    extract_years,
    match_resume_job,
)

models.Base.metadata.create_all(bind=engine)

SKILLS = load_skills()

app = FastAPI(title="智能简历岗位匹配系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- 启动时自动初始化内置岗位数据 ----
@app.on_event("startup")
def startup():
    from seed import seed_jobs
    seed_jobs()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# ==================== 简历接口 ====================

@app.post("/api/resumes")
def create_resume(data: schemas.ResumeCreate, db: Session = Depends(get_db)):
    if len(data.text) < 10 or len(data.text) > 5000:
        raise HTTPException(status_code=400, detail="简历原文长度应在10—5000字之间")
    skills = extract_skills(data.text, SKILLS)
    education = extract_education(data.text)
    years = extract_years(data.text)
    resume = models.Resume(
        name=data.name,
        text=data.text,
        skills=json.dumps(skills, ensure_ascii=False),
        education=education,
        years=years,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return {
        "id": resume.id,
        "name": resume.name,
        "skills": skills,
        "education": education,
        "years": years,
        "created_at": resume.created_at,
    }


@app.get("/api/resumes")
def list_resumes(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Resume).order_by(models.Resume.id.desc())
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {
        "total": total,
        "items": [
            {
                "id": r.id,
                "name": r.name,
                "skills": json.loads(r.skills),
                "education": r.education,
                "years": r.years,
                "created_at": r.created_at,
            }
            for r in items
        ],
    }


@app.get("/api/resumes/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="简历不存在")
    return {
        "id": r.id,
        "name": r.name,
        "text": r.text,
        "skills": json.loads(r.skills),
        "education": r.education,
        "years": r.years,
        "created_at": r.created_at,
    }


@app.delete("/api/resumes/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="简历不存在")
    db.delete(r)
    db.commit()
    return {"detail": "已删除"}


# ==================== 简历文件上传 ====================

ALLOWED_UPLOAD_EXTS = {".txt", ".doc", ".docx", ".pdf"}
MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB

# docx 的 WordprocessingML 命名空间
_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _extract_text_from_txt(data: bytes) -> str:
    for enc in ("utf-8", "gbk"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def _extract_text_from_docx(data: bytes) -> str:
    """解析 .docx（OOXML zip 包），按段落提取 word/document.xml 中的文本。"""
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            xml_content = z.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError):
        raise HTTPException(
            status_code=400,
            detail="无法解析该 Word 文件：老版 .doc 二进制格式暂不支持，请将文件另存为 .docx 后重新上传",
        )
    root = ET.fromstring(xml_content)
    paragraphs = []
    for p in root.iter(_W_NS + "p"):
        runs = [t.text or "" for t in p.iter(_W_NS + "t")]
        if runs:
            paragraphs.append("".join(runs))
    return "\n".join(paragraphs)


def _extract_text_from_pdf(data: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise HTTPException(status_code=500, detail="服务端缺少 pypdf 依赖，无法解析 PDF")
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = [(page.extract_text() or "") for page in reader.pages]
    except Exception:
        raise HTTPException(status_code=400, detail="PDF 文件解析失败，文件可能已损坏或为扫描件")
    return "\n".join(pages)


def _clean_extracted_text(text: str) -> str:
    text = re.sub(r"[ \t\u3000]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@app.post("/api/resumes/upload")
async def upload_resume(file: UploadFile = File(...)):
    """上传简历文件（Word/PDF/TXT），校验类型与大小后提取纯文本返回，由前端填入文本框供用户确认。"""
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_UPLOAD_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型「{ext or '无后缀'}」，仅允许上传 .doc / .docx / .pdf / .txt 文件",
        )

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="上传的文件内容为空")
    if len(data) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 2MB 限制，请压缩后重新上传")

    if ext == ".txt":
        text = _extract_text_from_txt(data)
    elif ext == ".pdf":
        text = _extract_text_from_pdf(data)
    else:
        text = _extract_text_from_docx(data)

    text = _clean_extracted_text(text)
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="文件中未提取到有效文本内容（可能为扫描版文件或空文档）")

    return {"filename": filename, "ext": ext, "size": len(data), "length": len(text), "text": text}


# ==================== 岗位接口 ====================

@app.post("/api/jobs")
def create_job(data: schemas.JobCreate, db: Session = Depends(get_db)):
    if len(data.text) < 10 or len(data.text) > 5000:
        raise HTTPException(status_code=400, detail="JD原文长度应在10—5000字之间")
    skills = extract_skills(data.text, SKILLS)
    education = extract_education(data.text)
    years = extract_years(data.text)
    job = models.Job(
        title=data.title,
        company=data.company,
        text=data.text,
        skills=json.dumps(skills, ensure_ascii=False),
        education=education,
        years=years,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "skills": skills,
        "education": education,
        "years": years,
        "created_at": job.created_at,
    }


@app.get("/api/jobs")
def list_jobs(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Job).order_by(models.Job.id.desc())
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {
        "total": total,
        "items": [
            {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "skills": json.loads(j.skills),
                "education": j.education,
                "years": j.years,
                "created_at": j.created_at,
            }
            for j in items
        ],
    }


@app.get("/api/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return {
        "id": j.id,
        "title": j.title,
        "company": j.company,
        "text": j.text,
        "skills": json.loads(j.skills),
        "education": j.education,
        "years": j.years,
        "created_at": j.created_at,
    }


@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    j = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="岗位不存在")
    db.delete(j)
    db.commit()
    return {"detail": "已删除"}


# ==================== 匹配接口 ====================

@app.post("/api/match")
def match(data: schemas.MatchRequest, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == data.resume_id).first()
    job = db.query(models.Job).filter(models.Job.id == data.job_id).first()
    if not resume or not job:
        raise HTTPException(status_code=404, detail="简历或岗位不存在")

    result = match_resume_job(resume, job)

    record = models.MatchRecord(
        resume_id=resume.id,
        job_id=job.id,
        score=result["score"],
        level=result["level"],
        skill_score=result["skill_score"],
        text_score=result["text_score"],
        edu_score=result["edu_score"],
        years_score=result["years_score"],
        matched_skills=json.dumps(result["matched_skills"], ensure_ascii=False),
        missing_skills=json.dumps(result["missing_skills"], ensure_ascii=False),
        suggestion=result["suggestion"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    result["id"] = record.id
    result["resume_id"] = resume.id
    result["job_id"] = job.id
    result["resume_name"] = resume.name
    result["job_title"] = job.title
    result["created_at"] = record.created_at
    return result


@app.post("/api/match/batch")
def batch_match(data: schemas.BatchMatchRequest, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == data.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")

    jobs = db.query(models.Job).all()
    results = []
    for job in jobs:
        result = match_resume_job(resume, job)
        record = models.MatchRecord(
            resume_id=resume.id,
            job_id=job.id,
            score=result["score"],
            level=result["level"],
            skill_score=result["skill_score"],
            text_score=result["text_score"],
            edu_score=result["edu_score"],
            years_score=result["years_score"],
            matched_skills=json.dumps(result["matched_skills"], ensure_ascii=False),
            missing_skills=json.dumps(result["missing_skills"], ensure_ascii=False),
            suggestion=result["suggestion"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        results.append(
            {
                "id": record.id,
                "resume_id": resume.id,
                "job_id": job.id,
                "job_title": job.title,
                "company": job.company,
                "score": result["score"],
                "level": result["level"],
                "skill_score": result["skill_score"],
                "text_score": result["text_score"],
                "edu_score": result["edu_score"],
                "years_score": result["years_score"],
                "matched_skills": result["matched_skills"],
                "missing_skills": result["missing_skills"],
                "suggestion": result["suggestion"],
                "created_at": record.created_at,
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"resume_id": resume.id, "resume_name": resume.name, "results": results}


# ==================== 历史记录接口 ====================

@app.get("/api/records")
def list_records(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.MatchRecord).order_by(models.MatchRecord.id.desc())
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    results = []
    for r in items:
        resume = db.query(models.Resume).filter(models.Resume.id == r.resume_id).first()
        job = db.query(models.Job).filter(models.Job.id == r.job_id).first()
        results.append(
            {
                "id": r.id,
                "resume_id": r.resume_id,
                "job_id": r.job_id,
                "resume_name": resume.name if resume else "已删除",
                "job_title": job.title if job else "已删除",
                "score": r.score,
                "level": r.level,
                "created_at": r.created_at,
            }
        )

    return {"total": total, "items": results}


@app.get("/api/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    r = db.query(models.MatchRecord).filter(models.MatchRecord.id == record_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="记录不存在")

    resume = db.query(models.Resume).filter(models.Resume.id == r.resume_id).first()
    job = db.query(models.Job).filter(models.Job.id == r.job_id).first()

    return {
        "id": r.id,
        "resume_id": r.resume_id,
        "job_id": r.job_id,
        "resume_name": resume.name if resume else "已删除",
        "job_title": job.title if job else "已删除",
        "score": r.score,
        "level": r.level,
        "skill_score": r.skill_score,
        "text_score": r.text_score,
        "edu_score": r.edu_score,
        "years_score": r.years_score,
        "matched_skills": json.loads(r.matched_skills),
        "missing_skills": json.loads(r.missing_skills),
        "suggestion": r.suggestion,
        "created_at": r.created_at,
    }


@app.delete("/api/records/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    r = db.query(models.MatchRecord).filter(models.MatchRecord.id == record_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(r)
    db.commit()
    return {"detail": "已删除"}


# ==================== 统计接口 ====================

@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    records = db.query(models.MatchRecord).all()
    total = len(records)
    avg_score = round(sum(r.score for r in records) / total, 1) if total else 0

    level_distribution = {"高度匹配": 0, "较匹配": 0, "一般": 0, "不匹配": 0}
    missing_counter = {}
    trend = {}

    for r in records:
        level_distribution[r.level] = level_distribution.get(r.level, 0) + 1
        for skill in json.loads(r.missing_skills):
            missing_counter[skill] = missing_counter.get(skill, 0) + 1
        date_str = r.created_at.strftime("%Y-%m-%d") if r.created_at else ""
        trend[date_str] = trend.get(date_str, 0) + 1

    top5 = sorted(missing_counter.items(), key=lambda x: x[1], reverse=True)[:5]
    trend_data = sorted(trend.items())[-7:]

    return {
        "total": total,
        "avg_score": avg_score,
        "level_distribution": level_distribution,
        "missing_skill_top5": [{"skill": k, "count": v} for k, v in top5],
        "trend": [{"date": k, "count": v} for k, v in trend_data],
    }