from typing import List
from ..schemas.role_match import RoleArchetype

TECH_ROLES_DATASET: List[RoleArchetype] = [
    RoleArchetype(
        id="backend-engineer",
        title="Backend Software Engineer",
        category="Software Engineering",
        description="Designs, builds, and maintains server-side architecture, RESTful and GraphQL APIs, database schemas, caching layers, and high-throughput microservices. Focuses on scalability, reliability, and security.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "REST APIs", "SQL", "Git", "Docker", "Data Structures"],
        preferred_skills=["Redis", "Kubernetes", "Celery", "Kafka", "AWS", "CI/CD", "System Design", "gRPC", "Microservices"],
        typical_tools=["FastAPI", "Django", "Node.js", "Go", "PostgreSQL", "Redis", "Docker", "AWS ECS", "GitHub Actions"],
        experience_levels=["Junior", "Mid-Level", "Senior", "Staff"],
        market_demand="Very High",
        average_salary_range="$110,000 - $175,000"
    ),
    RoleArchetype(
        id="fullstack-developer",
        title="Full-Stack Developer",
        category="Software Engineering",
        description="Bridges client-facing interfaces with server-side business logic. Develops end-to-end web applications with responsive UIs, robust backend APIs, relational/NoSQL databases, and automated deployments.",
        required_skills=["JavaScript", "TypeScript", "React", "Python", "Node.js", "HTML", "CSS", "SQL", "REST APIs", "Git"],
        preferred_skills=["Next.js", "Tailwind CSS", "FastAPI", "PostgreSQL", "Docker", "AWS", "GraphQL", "Redis", "State Management"],
        typical_tools=["React", "Next.js", "TypeScript", "FastAPI", "Express", "PostgreSQL", "Vite", "Vercel", "Docker"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="Very High",
        average_salary_range="$105,000 - $165,000"
    ),
    RoleArchetype(
        id="frontend-engineer",
        title="Frontend Web Engineer",
        category="Software Engineering",
        description="Creates intuitive, high-performance, and visually responsive user interfaces. Specializes in modern JavaScript/TypeScript ecosystems, component architecture, state management, and web performance optimization.",
        required_skills=["JavaScript", "TypeScript", "React", "HTML", "CSS", "Responsive Design", "Git", "REST APIs"],
        preferred_skills=["Next.js", "Tailwind CSS", "Redux", "Zustand", "Webpack", "Vite", "Web Performance", "Accessibility (a11y)", "Jest"],
        typical_tools=["React", "Next.js", "TypeScript", "Tailwind CSS", "Figma", "Vite", "Storybook", "Jest"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$100,000 - $160,000"
    ),
    RoleArchetype(
        id="ai-ml-engineer",
        title="AI / Machine Learning Engineer",
        category="Artificial Intelligence",
        description="Develops, trains, fine-tunes, and deploys machine learning and deep learning models. Implements NLP, LLMs, computer vision, feature pipelines, and model evaluation benchmarks.",
        required_skills=["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Machine Learning", "Deep Learning", "Mathematics & Statistics", "SQL", "Git"],
        preferred_skills=["HuggingFace", "Transformers", "LLMs", "RAG", "Embeddings", "LangChain", "Vector Databases", "Model Fine-tuning", "ONNX"],
        typical_tools=["PyTorch", "HuggingFace", "ChromaDB", "FAISS", "Jupyter", "Weights & Biases", "CUDA", "FastAPI"],
        experience_levels=["Junior", "Mid-Level", "Senior", "Lead"],
        market_demand="Very High",
        average_salary_range="$130,000 - $210,000"
    ),
    RoleArchetype(
        id="mlops-engineer",
        title="MLOps / LLM Systems Engineer",
        category="Artificial Intelligence",
        description="Specializes in productionizing AI/ML models. Builds scalable inference engines, automated CI/CD for model retraining, monitoring pipelines for model drift, vector search infrastructure, and GPU orchestration.",
        required_skills=["Python", "Docker", "Kubernetes", "Machine Learning", "FastAPI", "CI/CD", "Cloud (AWS/GCP)", "Git"],
        preferred_skills=["MLflow", "Kubeflow", "Triton Inference Server", "Ray", "vLLM", "Vector DBs (Qdrant/Milvus/Chroma)", "Terraform", "Prometheus"],
        typical_tools=["Docker", "Kubernetes", "MLflow", "vLLM", "AWS SageMaker", "ChromaDB", "FastAPI", "Grafana"],
        experience_levels=["Mid-Level", "Senior", "Staff"],
        market_demand="Very High",
        average_salary_range="$140,000 - $220,000"
    ),
    RoleArchetype(
        id="data-engineer",
        title="Data Engineer",
        category="Data & Analytics",
        description="Designs and builds scalable data ingestion pipelines, ETL/ELT workflows, data warehouses, and streaming architectures to power analytics and machine learning applications.",
        required_skills=["Python", "SQL", "Data Warehousing", "ETL Pipelines", "PostgreSQL", "Git", "Data Modeling"],
        preferred_skills=["Apache Spark", "Airflow", "Kafka", "Snowflake", "dbt", "BigQuery", "AWS S3 / Redshift", "Databricks", "Distributed Computing"],
        typical_tools=["Apache Airflow", "Spark", "PostgreSQL", "Snowflake", "dbt", "Kafka", "Docker", "AWS Glue"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$115,000 - $180,000"
    ),
    RoleArchetype(
        id="devops-cloud-engineer",
        title="DevOps & Cloud Platform Engineer",
        category="Infrastructure & Cloud",
        description="Manages cloud infrastructure, automates continuous integration and continuous deployment (CI/CD) pipelines, orchestrates container clusters, and implements Infrastructure as Code (IaC).",
        required_skills=["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Bash / Shell", "Git", "Networking & Security"],
        preferred_skills=["Terraform", "Ansible", "GitHub Actions", "ArgoCD", "GCP", "Azure", "Helm", "Prometheus & Grafana", "IAM"],
        typical_tools=["Terraform", "Kubernetes", "Docker", "GitHub Actions", "AWS", "Prometheus", "Linux", "Helm"],
        experience_levels=["Mid-Level", "Senior", "Lead"],
        market_demand="High",
        average_salary_range="$120,000 - $185,000"
    ),
    RoleArchetype(
        id="data-scientist",
        title="Data Scientist",
        category="Data & Analytics",
        description="Analyzes complex business datasets to uncover patterns, build predictive statistical models, design A/B experiments, and translate data insights into strategic product decisions.",
        required_skills=["Python", "SQL", "Pandas", "NumPy", "Statistics & Probability", "Data Visualization", "Scikit-Learn", "Git"],
        preferred_skills=["A/B Testing", "Machine Learning", "Tableau / PowerBI", "Hypothesis Testing", "Time Series Analysis", "PySpark", "Feature Engineering"],
        typical_tools=["Jupyter", "Pandas", "Scikit-Learn", "Matplotlib / Seaborn", "Tableau", "SQL", "R"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="Steady",
        average_salary_range="$110,000 - $170,000"
    ),
    RoleArchetype(
        id="mobile-engineer",
        title="Mobile App Engineer (Cross-Platform / Native)",
        category="Software Engineering",
        description="Builds fluid, responsive, and resilient mobile applications for iOS and Android platforms using modern cross-platform frameworks or native toolchains.",
        required_skills=["JavaScript / TypeScript", "React Native", "Mobile UI/UX", "REST APIs", "State Management", "Git"],
        preferred_skills=["Flutter / Dart", "Swift / iOS", "Kotlin / Android", "App Store & Play Store Deployment", "Offline Storage", "Firebase", "CI/CD for Mobile"],
        typical_tools=["React Native", "Expo", "Flutter", "Xcode", "Android Studio", "Firebase", "TypeScript"],
        experience_levels=["Junior", "Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$105,000 - $165,000"
    ),
    RoleArchetype(
        id="cybersecurity-engineer",
        title="Application Security & Cybersecurity Engineer",
        category="Security & Infrastructure",
        description="Secures applications, networks, and cloud environments against vulnerabilities, conducts threat modeling, implements authentication/authorization protocols, and enforces compliance standards.",
        required_skills=["Networking & Protocols", "Linux", "Security Fundamentals", "OWASP Top 10", "Python / Bash", "Git"],
        preferred_skills=["Threat Modeling", "Penetration Testing", "Cloud Security (AWS/Azure)", "SIEM / SOC", "Cryptography", "Container Security", "SAST/DAST"],
        typical_tools=["Burp Suite", "Wireshark", "SonarQube", "Trivy", "Splunk", "AWS GuardDuty", "Linux"],
        experience_levels=["Mid-Level", "Senior"],
        market_demand="High",
        average_salary_range="$120,000 - $190,000"
    )
]
