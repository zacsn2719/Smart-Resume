import re
import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_DICT_PATH = "skill_dict.txt"

SKILL_SET = None


def load_skills(path=SKILL_DICT_PATH):
    global SKILL_SET
    with open(path, "r", encoding="utf-8") as f:
        SKILL_SET = set(line.strip() for line in f if line.strip())
    for skill in SKILL_SET:
        jieba.add_word(skill)
    return SKILL_SET


def get_skills():
    global SKILL_SET
    if SKILL_SET is None:
        load_skills()
    return SKILL_SET


def extract_skills(text, skill_set=None):
    """基于技能词典的词边界匹配，避免 C/Go 等短词误命中（如 django 中的 go）。"""
    if skill_set is None:
        skill_set = get_skills()
    found = set()
    for skill in skill_set:
        pattern = r"(?<![A-Za-z0-9+#.])" + re.escape(skill) + r"(?![A-Za-z0-9+#])"
        if re.search(pattern, text, re.IGNORECASE):
            found.add(skill)
    return sorted(found)


def extract_education(text):
    if "博士" in text:
        return "博士"
    if "硕士" in text or "研究生" in text:
        return "硕士"
    if "本科" in text or "学士" in text:
        return "本科"
    if "专科" in text or "大专" in text:
        return "专科"
    return "不限"


def extract_years(text):
    """抽取工作年限，优先匹配经验类表达，泛匹配时排除 2023年 这类日期。"""
    patterns = [r"(\d+)\s*年经验", r"工作\s*(\d+)\s*年", r"(\d+)\s*年以上"]
    for p in patterns:
        m = re.search(p, text)
        if m:
            v = int(m.group(1))
            if 1 <= v <= 50:
                return v
    m = re.search(r"(\d+)\s*年", text)
    if m:
        v = int(m.group(1))
        if 1 <= v <= 50:
            return v
    return 0


def jieba_tokenize(text):
    return list(jieba.cut(text))


def text_similarity(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, token_pattern=None)
    try:
        tfidf = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0


def calc_edu_score(resume_edu, job_edu):
    order = {"不限": 0, "专科": 1, "本科": 2, "硕士": 3, "博士": 4}
    r = order.get(resume_edu, 0)
    j = order.get(job_edu, 0)
    if j == 0 or r >= j:
        return 1.0
    return 0.5


def calc_years_score(resume_years, job_years):
    if job_years <= 0:
        return 1.0
    diff = job_years - resume_years
    if diff <= 0:
        return 1.0
    if diff == 1:
        return 0.7
    if diff == 2:
        return 0.4
    return 0.2


def build_suggestion(missing_skills, edu_score, years_score, text_score):
    parts = []
    if missing_skills:
        parts.append("建议补充 " + "、".join(missing_skills[:3]) + " 项目经验。")
    if edu_score < 1:
        parts.append("建议突出相关课程、项目或继续教育经历。")
    if years_score < 1:
        parts.append("建议强化项目深度和实习经历。")
    if text_score < 0.3:
        parts.append("建议在简历中使用岗位 JD 中的关键词。")
    return "".join(parts) or "简历与岗位匹配良好，可进一步突出项目成果。"


def match_resume_job(resume, job):
    resume_skills = set(json.loads(resume.skills))
    job_skills = set(json.loads(job.skills))

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    skill_score = len(matched) / len(job_skills) if job_skills else 1.0

    text_score = text_similarity(resume.text, job.text)
    edu_score = calc_edu_score(resume.education, job.education)
    years_score = calc_years_score(resume.years, job.years)

    score = round((skill_score * 0.4 + text_score * 0.3 + edu_score * 0.2 + years_score * 0.1) * 100, 1)

    if score >= 80:
        level = "高度匹配"
    elif score >= 65:
        level = "较匹配"
    elif score >= 50:
        level = "一般"
    else:
        level = "不匹配"

    suggestion = build_suggestion(missing, edu_score, years_score, text_score)

    return {
        "score": score,
        "level": level,
        "skill_score": round(skill_score, 4),
        "text_score": round(text_score, 4),
        "edu_score": edu_score,
        "years_score": years_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestion": suggestion
    }