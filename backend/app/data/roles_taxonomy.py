from typing import List
from ..schemas.role_match import RoleArchetype

TECH_ROLES_DATASET: List[RoleArchetype] = [
    RoleArchetype(
        id="data-analyst-bi",
        title="Data Analyst & BI Engineer",
        category="Data & Analytics",
        description="Extracts, analyzes, and visualizes complex datasets to drive business decisions. Builds interactive Power BI/Tableau dashboards, executes advanced SQL queries, and translates raw metrics into strategic executive insights.",
        required_skills=["SQL", "Python", "Power BI", "Data Analysis", "Pandas", "Data Visualization", "Dashboards"],
        preferred_skills=["Tableau", "NumPy", "Matplotlib", "Seaborn", "Machine Learning", "CRM / Salesforce", "Statistical Analysis", "Business Analysis"],
        typical_tools=["Power BI", "SQL", "Python", "Pandas", "Tableau", "Jupyter", "Excel", "PostgreSQL"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="Very High",
        average_salary_range="$85,000 - $140,000"
    ),
    RoleArchetype(
        id="ai-ml-engineer",
        title="AI / Machine Learning Engineer",
        category="Artificial Intelligence",
        description="Develops, trains, fine-tunes, and deploys machine learning and deep learning models. Implements NLP, LLMs, computer vision, feature pipelines, vector search, and model evaluation benchmarks.",
        required_skills=["Python", "Machine Learning", "Deep Learning", "SQL", "Scikit-Learn", "RAG", "Embeddings"],
        preferred_skills=["PyTorch", "TensorFlow", "HuggingFace", "Transformers", "LLMs", "LangChain", "Vector Databases", "ChromaDB", "FastAPI"],
        typical_tools=["Python", "PyTorch", "HuggingFace", "ChromaDB", "FAISS", "LangChain", "Jupyter", "FastAPI"],
        experience_levels=["Junior", "Mid-Level", "Senior", "Lead"],
        market_demand="Very High",
        average_salary_range="$130,000 - $210,000"
    ),
    RoleArchetype(
        id="backend-engineer",
        title="Backend Software Engineer",
        category="Software Engineering",
        description="Designs, builds, and maintains server-side architecture, RESTful APIs, database schemas, caching layers, and microservices. Focuses on scalability, reliability, and performance.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "REST APIs", "SQL", "Docker"],
        preferred_skills=["Redis", "Kubernetes", "Celery", "Kafka", "AWS", "CI/CD", "System Design", "Git", "Microservices"],
        typical_tools=["FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "AWS", "GitHub Actions", "Python"],
        experience_levels=["Junior", "Mid-Level", "Senior", "Staff"],
        market_demand="Very High",
        average_salary_range="$110,000 - $175,000"
    ),
    RoleArchetype(
        id="mlops-engineer",
        title="MLOps / LLM Systems Engineer",
        category="Artificial Intelligence",
        description="Specializes in productionizing AI/ML and LLM pipelines. Builds scalable inference engines, automated retraining, vector search infrastructure, and model monitoring.",
        required_skills=["Python", "Docker", "Machine Learning", "FastAPI", "RAG", "Vector Databases"],
        preferred_skills=["Kubernetes", "MLflow", "CI/CD", "vLLM", "ChromaDB", "LangChain", "Cloud (AWS/GCP)", "Prometheus"],
        typical_tools=["Docker", "Kubernetes", "MLflow", "ChromaDB", "FastAPI", "Python", "LangChain", "Grafana"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="Very High",
        average_salary_range="$140,000 - $220,000"
    ),
    RoleArchetype(
        id="data-scientist",
        title="Data Scientist",
        category="Data & Analytics",
        description="Analyzes complex business datasets to uncover patterns, build predictive statistical models, design A/B experiments, and translate data insights into strategic product decisions.",
        required_skills=["Python", "SQL", "Pandas", "NumPy", "Statistics & Probability", "Data Visualization", "Scikit-Learn"],
        preferred_skills=["Machine Learning", "Tableau / PowerBI", "Feature Engineering", "A/B Testing", "Deep Learning", "Seaborn"],
        typical_tools=["Jupyter", "Pandas", "Scikit-Learn", "Matplotlib / Seaborn", "Power BI", "SQL"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$110,000 - $170,000"
    ),
    RoleArchetype(
        id="data-engineer",
        title="Data Engineer",
        category="Data & Analytics",
        description="Designs and builds scalable data ingestion pipelines, ETL/ELT workflows, data warehouses, and streaming architectures to power analytics and machine learning applications.",
        required_skills=["Python", "SQL", "Data Warehousing", "ETL Pipelines", "PostgreSQL"],
        preferred_skills=["Apache Spark", "Airflow", "Kafka", "Docker", "dbt", "Snowflake", "Data Modeling"],
        typical_tools=["Apache Airflow", "Spark", "PostgreSQL", "Snowflake", "dbt", "Kafka", "Docker"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$115,000 - $180,000"
    ),
    RoleArchetype(
        id="fullstack-developer",
        title="Full-Stack Developer",
        category="Software Engineering",
        description="Bridges client-facing interfaces with server-side business logic. Develops end-to-end web applications with responsive UIs, backend APIs, databases, and deployments.",
        required_skills=["JavaScript", "TypeScript", "React", "Python", "Node.js", "SQL", "REST APIs"],
        preferred_skills=["Next.js", "Tailwind CSS", "FastAPI", "PostgreSQL", "Docker", "AWS", "GraphQL", "Redis"],
        typical_tools=["React", "Next.js", "TypeScript", "FastAPI", "Express", "PostgreSQL", "Docker"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="Very High",
        average_salary_range="$105,000 - $165,000"
    ),
    RoleArchetype(
        id="frontend-engineer",
        title="Frontend Web Engineer",
        category="Software Engineering",
        description="Creates intuitive, high-performance, and visually responsive user interfaces with modern component architectures and state management.",
        required_skills=["JavaScript", "TypeScript", "React", "HTML", "CSS", "Responsive Design", "REST APIs"],
        preferred_skills=["Next.js", "Tailwind CSS", "Redux", "Zustand", "Vite", "Web Performance", "Jest"],
        typical_tools=["React", "Next.js", "TypeScript", "Tailwind CSS", "Figma", "Vite"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$100,000 - $160,000"
    ),
    RoleArchetype(
        id="devops-cloud-engineer",
        title="DevOps & Cloud Platform Engineer",
        category="Infrastructure & Cloud",
        description="Automates infrastructure provisioning, continuous integration & continuous deployment (CI/CD) pipelines, and container cluster orchestration.",
        required_skills=["Linux", "Docker", "Kubernetes", "AWS", "CI/CD"],
        preferred_skills=["Terraform", "GitHub Actions", "GCP", "Prometheus & Grafana", "Networking & Security"],
        typical_tools=["Terraform", "Kubernetes", "Docker", "GitHub Actions", "AWS", "Linux"],
        experience_levels=["Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$120,000 - $185,000"
    ),
    RoleArchetype(
        id="mobile-engineer",
        title="Mobile App Engineer",
        category="Software Engineering",
        description="Builds responsive, resilient mobile applications for iOS and Android platforms using cross-platform frameworks or native toolchains.",
        required_skills=["JavaScript / TypeScript", "React Native", "Mobile UI/UX", "REST APIs"],
        preferred_skills=["Flutter", "Swift", "Kotlin", "Offline Storage", "Firebase", "CI/CD"],
        typical_tools=["React Native", "Expo", "Flutter", "Xcode", "Android Studio"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$105,000 - $165,000"
    )
]
