import json
from database import SessionLocal, engine
from models import Base, Job
from ai_service import load_skills, extract_skills, extract_education, extract_years


def seed_jobs():
    load_skills()
    db = SessionLocal()
    existing = db.query(Job).count()
    if existing > 0:
        db.close()
        return

    jobs = [
        {
            "title": "Python后端开发",
            "company": "ABC科技",
            "text": "本科及以上学历,3年以上Python开发经验。熟悉Django/Flask/FastAPI框架,掌握MySQL、PostgreSQL数据库,熟练使用Redis缓存和Docker容器化部署。了解Linux系统管理,具备良好的代码规范。"
        },
        {
            "title": "前端开发工程师",
            "company": "XYZ网络",
            "text": "本科及以上学历,2年以上前端开发经验。精通HTML、CSS、JavaScript,熟练使用Vue或React框架,了解Webpack/Vite构建工具,熟悉RESTful API对接。"
        },
        {
            "title": "数据分析师",
            "company": "数据洞察科技",
            "text": "本科及以上学历,2年以上数据分析经验。熟练使用Python、SQL、Pandas、NumPy进行数据处理和分析,熟悉Tableau或Power BI等可视化工具,了解机器学习基础。"
        },
        {
            "title": "AI应用开发工程师",
            "company": "智联AI",
            "text": "硕士及以上学历,3年以上AI开发经验。精通Python、PyTorch或TensorFlow框架,熟悉NLP/机器学习和深度学习算法,有模型训练和部署经验,了解Docker和Kubernetes。"
        },
        {
            "title": "测试开发工程师",
            "company": "质量先锋",
            "text": "本科及以上学历,2年以上测试开发经验。熟悉Python或Java编程,掌握Selenium/JUnit测试框架,了解CI/CD和Jenkins,有自动化测试平台开发经验。"
        },
        {
            "title": "Java后端开发",
            "company": "云端软件",
            "text": "本科及以上学历,3年以上Java开发经验。精通Spring Boot/MyBatis框架,熟悉MySQL/Redis/Elasticsearch,了解微服务架构和Docker/Kubernetes,有高性能系统设计经验。"  
        },
        {
            "title": "产品经理",
            "company": "创新工厂",
            "text": "本科及以上学历,2年以上产品经验。熟悉产品设计和项目管理流程,具备用户研究和数据分析能力,熟练使用Figma/Sketch等原型工具,有敏捷开发经验。"
        },
        {
            "title": "运维开发工程师",
            "company": "云盾科技",
            "text": "本科及以上学历,3年以上运维开发经验。精通Linux系统管理,熟悉Docker/Kubernetes容器编排,掌握Python/Shell脚本编程,了解CI/CD和Jenkins,有监控告警平台搭建经验。"
        }
    ]

    for j in jobs:
        skills = extract_skills(j["text"])
        education = extract_education(j["text"])
        years = extract_years(j["text"])
        job = Job(
            title=j["title"],
            company=j["company"],
            text=j["text"],
            skills=json.dumps(skills, ensure_ascii=False),
            education=education,
            years=years
        )
        db.add(job)

    db.commit()
    db.close()
    print(f"已初始化 {len(jobs)} 个内置岗位。")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_jobs()
    print("数据库初始化完成。")