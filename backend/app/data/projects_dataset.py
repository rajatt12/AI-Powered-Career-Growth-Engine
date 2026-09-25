from typing import List
from ..schemas.projects import ProjectTemplate

PROJECTS_DATASET: List[ProjectTemplate] = [
    ProjectTemplate(
        id="distributed-task-queue",
        title="Distributed Asynchronous Task Queue & Job Scheduler",
        tagline="A resilient background task processing system handling millions of jobs with retry logic, rate limiting, and failure alerts.",
        difficulty="Intermediate",
        estimated_hours=25,
        target_roles=["backend-engineer", "fullstack-developer", "devops-cloud-engineer"],
        skills_covered=["Python", "FastAPI", "Redis", "Celery", "Docker", "PostgreSQL", "System Design"],
        architecture_overview="Clients submit compute-intensive tasks via a FastAPI gateway. Tasks are queued in a Redis broker and consumed by an elastic pool of asynchronous Celery workers, storing results and execution metrics in PostgreSQL.",
        system_architecture_mermaid="""graph LR
    Client([Client App]) -->|POST /tasks| API[FastAPI Gateway]
    API -->|Enqueue Task| Redis[(Redis Broker)]
    Redis -->|Dispatch Job| W1[Celery Worker 1]
    Redis -->|Dispatch Job| W2[Celery Worker 2]
    W1 -->|Save Results| DB[(PostgreSQL)]
    W2 -->|Save Results| DB
    API -->|GET /tasks/status| DB""",
        core_features=[
            "Non-blocking asynchronous task execution with exponential backoff retry mechanism",
            "Redis-backed token-bucket rate limiter per API key",
            "Dead-Letter Queue (DLQ) for inspecting and replaying failed background jobs",
            "Interactive monitoring dashboard showing real-time queue depth and worker throughput"
        ],
        database_models=["Task (id, user_id, task_type, payload, status, created_at, completed_at, retry_count)", "WorkerMetric (id, worker_id, cpu_usage, memory_mb, active_jobs)"],
        resume_bullet_points=[
            "Engineered a distributed background task engine with FastAPI, Celery, and Redis, reducing API blocking time by 75% for 100k+ daily background jobs.",
            "Implemented exponential backoff retry policies and Dead-Letter Queues (DLQ), boosting job completion reliability to 99.95%.",
            "Containerized the worker cluster with Docker and automated health monitoring via Redis heartbeat metrics."
        ],
        github_starter_topics=["fastapi", "celery", "redis", "distributed-systems", "docker"]
    ),
    ProjectTemplate(
        id="realtime-collaborative-workspace",
        title="Real-Time Collaborative Document Canvas & Sync Engine",
        tagline="Multi-user collaborative workspace with conflict-free concurrent editing, WebSockets, and presence indicators.",
        difficulty="Advanced",
        estimated_hours=35,
        target_roles=["fullstack-developer", "frontend-engineer", "backend-engineer"],
        skills_covered=["TypeScript", "React", "Next.js", "WebSockets", "Redis", "FastAPI", "PostgreSQL", "Tailwind CSS"],
        architecture_overview="A full-stack reactive workspace where multiple clients establish bidirectional WebSocket channels to synchronize canvas/document states via Redis Pub/Sub pub-sub clusters.",
        system_architecture_mermaid="""graph TD
    U1[User 1 Browser] <-->|WebSocket| WS[WebSocket Server]
    U2[User 2] <-->|WebSocket| WS
    WS <-->|Pub/Sub Sync| Redis[(Redis Pub/Sub)]
    WS -->|Periodic Snapshot| DB[(PostgreSQL Database)]""",
        core_features=[
            "Low-latency document state replication using Operational Transformation (OT) or CRDTs",
            "Real-time user presence tracking (live cursor movements and active collaborator avatars)",
            "Revision history with point-in-time document snapshot restorations",
            "Responsive UI with glassmorphic dark theme and optimistic UI updates"
        ],
        database_models=["Document (id, title, content_snapshot, owner_id, version, updated_at)", "DocumentRevision (id, document_id, diff, author_id, created_at)"],
        resume_bullet_points=[
            "Architected a real-time collaborative workspace using WebSockets, Redis Pub/Sub, and Next.js, achieving sub-40ms state synchronization latency.",
            "Designed a Conflict-Free Replicated Data Type (CRDT) engine to handle concurrent multi-user edits without state divergence.",
            "Built automated snapshotting to PostgreSQL, optimizing network payload size by 60% using incremental diff compression."
        ],
        github_starter_topics=["nextjs", "websockets", "redis-pubsub", "collaborative-editing", "typescript"]
    ),
    ProjectTemplate(
        id="production-rag-agent",
        title="Enterprise Knowledge RAG Engine & Autonomous Research Agent",
        tagline="Production-grade Retrieval-Augmented Generation platform with semantic vector search, citation verification, and structured LLM tool-calling.",
        difficulty="Advanced",
        estimated_hours=30,
        target_roles=["ai-ml-engineer", "mlops-engineer", "backend-engineer"],
        skills_covered=["Python", "PyTorch", "HuggingFace", "ChromaDB", "RAG", "Embeddings", "FastAPI", "Docker", "LLMs"],
        architecture_overview="Ingests enterprise documents (PDFs, Markdown, Webpages), creates dense embeddings via text-embedding-004, stores them in ChromaDB, and performs hybrid dense/sparse retrieval with contextual reranking to ground LLM reasoning.",
        system_architecture_mermaid="""graph LR
    Doc[Enterprise Documents] --> Splitter[Recursive Chunking]
    Splitter --> Embed[Embedding Model]
    Embed --> VDB[(ChromaDB Vector Store)]
    User[User Query] --> VDB
    VDB -->|Top-K Grounded Chunks| Prompt[RAG Prompt Assembly]
    Prompt --> LLM[Google Gemini / LLM]
    LLM --> Answer([Structured Response with Citations])""",
        core_features=[
            "Layout-aware multi-modal document ingestion and recursive text chunking with token overlap",
            "Vector similarity search with metadata filtering and reciprocal rank fusion (RRF)",
            "Strict hallucination guardrails using source citation verification and structured JSON schemas",
            "REST API with streaming responses (Server-Sent Events) and latency benchmarking"
        ],
        database_models=["DocumentChunk (id, document_id, chunk_text, embedding_vector, metadata_json)", "QueryLog (id, query_text, retrieved_sources, latency_ms, tokens_used)"],
        resume_bullet_points=[
            "Built an enterprise RAG knowledge engine using ChromaDB, Gemini LLM, and FastAPI, achieving 94% citation accuracy on 10,000+ technical docs.",
            "Implemented hybrid dense-sparse vector retrieval with chunk reranking, reducing retrieval hallucinations by 65%.",
            "Dockerized the microservice and deployed SSE streaming endpoints delivering sub-500ms time-to-first-token."
        ],
        github_starter_topics=["rag", "chromadb", "llm", "fastapi", "generative-ai"]
    ),
    ProjectTemplate(
        id="mlops-retraining-pipeline",
        title="End-to-End MLOps Model Training, Inference & Drift Monitoring Platform",
        tagline="Automated continuous training pipeline with experiment tracking, canary deployments, and real-time data drift monitoring.",
        difficulty="Advanced",
        estimated_hours=35,
        target_roles=["mlops-engineer", "ai-ml-engineer", "data-engineer", "devops-cloud-engineer"],
        skills_covered=["Python", "Docker", "Kubernetes", "MLflow", "FastAPI", "CI/CD", "Prometheus", "Machine Learning"],
        architecture_overview="Orchestrates automated retraining pipelines triggered by data drift metrics. Tracks experiments and model registry artifacts in MLflow, package models into containerized FastAPI inference servers with Prometheus metrics.",
        system_architecture_mermaid="""graph TD
    Data[New Ingested Data] --> Drift[Drift Detector / Evidently]
    Drift -->|Drift Threshold Exceeded| Train[Retraining Pipeline]
    Train --> Reg[MLflow Model Registry]
    Reg -->|Canary Release| K8s[Kubernetes Cluster / FastAPI]
    K8s -->|Live Latency & Metrics| Prom[(Prometheus / Grafana)]""",
        core_features=[
            "Automated model lineage and artifact versioning with MLflow Model Registry",
            "Real-time Kolmogorov-Smirnov statistical testing for input feature drift detection",
            "Zero-downtime canary deployment strategy on Kubernetes clusters",
            "Production latency and throughput dashboard via Prometheus and Grafana exporters"
        ],
        database_models=["ExperimentRun (id, run_name, model_type, train_loss, val_f1, artifact_path)", "DriftAlert (id, feature_name, p_value, triggered_at, status)"],
        resume_bullet_points=[
            "Engineered an automated MLOps continuous retraining pipeline using MLflow and Docker, reducing model deployment cycle time from weeks to hours.",
            "Designed statistical data drift detectors with Prometheus alerts, ensuring production model accuracy remained above 93%.",
            "Deployed scalable FastAPI inference endpoints on Kubernetes handling 2,000 requests/sec with p99 latency under 45ms."
        ],
        github_starter_topics=["mlops", "mlflow", "kubernetes", "docker", "machine-learning"]
    ),
    ProjectTemplate(
        id="event-driven-analytics-pipeline",
        title="Real-Time Event Streaming & Scalable Analytics Engine",
        tagline="High-throughput streaming ETL pipeline ingesting high-velocity clickstream and telemetry events into columnar data warehouses.",
        difficulty="Advanced",
        estimated_hours=30,
        target_roles=["data-engineer", "backend-engineer"],
        skills_covered=["Python", "SQL", "Kafka", "PostgreSQL", "Docker", "ETL Pipelines", "Data Modeling"],
        architecture_overview="Simulates thousands of concurrent IoT or web events emitted to an Apache Kafka topic, consumed by Python stream processors, cleaned, aggregated into windowed metrics, and persisted into PostgreSQL/Snowflake.",
        system_architecture_mermaid="""graph LR
    Events[Event Producers] -->|JSON Stream| Kafka[(Apache Kafka Cluster)]
    Kafka --> Consumer[Python Stream Processor]
    Consumer -->|Batch Aggregations| DB[(PostgreSQL Data Warehouse)]
    DB --> Analytics[Analytics API & Dashboard]""",
        core_features=[
            "Partitioned Kafka topic architecture with consumer group scaling",
            "Sliding-window time aggregations and schema validation with Pydantic",
            "Idempotent database upserts preventing duplicate event processing during network disconnects",
            "SQL data modeling with dimensional star schema (Fact and Dimension tables)"
        ],
        database_models=["FactEvent (id, event_type, user_id, timestamp, duration_ms, device_type)", "DimUser (id, country, tier, signup_date)"],
        resume_bullet_points=[
            "Built a distributed event-driven data pipeline using Apache Kafka and Python, reliably ingesting 5M+ events/day with zero data loss.",
            "Implemented sliding-window aggregations and idempotent PostgreSQL writes, reducing analytical query response time by 70%.",
            "Containerized the entire multi-broker Kafka and Zookeeper topology using Docker Compose."
        ],
        github_starter_topics=["kafka", "etl", "data-engineering", "python", "sql"]
    ),
    ProjectTemplate(
        id="cloud-iac-kubernetes-cluster",
        title="Multi-Environment Cloud Infrastructure as Code (IaC) & Microservice Mesh",
        tagline="Declarative cloud infrastructure provisioning with Terraform, automated GitHub Actions CI/CD, and Kubernetes cluster orchestration.",
        difficulty="Advanced",
        estimated_hours=25,
        target_roles=["devops-cloud-engineer", "backend-engineer"],
        skills_covered=["AWS", "Terraform", "Kubernetes", "Docker", "CI/CD", "Linux", "Networking & Security"],
        architecture_overview="Defines production-ready AWS infrastructure (VPC, Subnets, EKS, RDS, S3, IAM) completely in modular Terraform code, coupled with GitHub Actions CI/CD pipelines deploying containerized microservices.",
        system_architecture_mermaid="""graph TD
    Git[GitHub Commit] --> Actions[GitHub Actions CI/CD]
    Actions -->|Terraform Apply| AWS[AWS Cloud VPC / IAM]
    Actions -->|Build & Push Image| ECR[Container Registry]
    ECR -->|Deploy Manifest| EKS[Amazon EKS Kubernetes]
    EKS -->|State Metrics| Mon[Prometheus & Grafana]""",
        core_features=[
            "Modular Terraform definitions for VPC peering, private subnets, and least-privilege IAM policies",
            "Automated Helm chart deployments with Horizontal Pod Autoscalers (HPA) based on CPU/memory load",
            "Encrypted secret management using AWS Secrets Manager and Kubernetes SealedSecrets",
            "Automated semantic release and multi-stage Docker build optimizations (<50MB image size)"
        ],
        database_models=["InfraState (environment, terraform_version, last_applied_by, resources_count)"],
        resume_bullet_points=[
            "Provisioned secure, repeatable multi-environment AWS infrastructure using Terraform IaC, cutting cloud provisioning time by 85%.",
            "Architected a Kubernetes (EKS) microservice cluster with Horizontal Pod Autoscaling, maintaining 99.99% uptime during traffic surges.",
            "Built secure GitHub Actions CI/CD pipelines with multi-stage Docker caching and automated vulnerability scans using Trivy."
        ],
        github_starter_topics=["terraform", "kubernetes", "aws", "devops", "ci-cd"]
    ),
    ProjectTemplate(
        id="ecommerce-rate-limited-api",
        title="High-Concurrency E-Commerce Platform API with Cache Invalidation & Rate Limiting",
        tagline="Production REST API architecture featuring Redis multi-layer caching, database connection pooling, and resilient transaction management.",
        difficulty="Intermediate",
        estimated_hours=20,
        target_roles=["backend-engineer", "fullstack-developer"],
        skills_covered=["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "REST APIs", "SQL"],
        architecture_overview="High-performance backend API serving product catalogs, inventory management, and cart checkouts. Employs write-through caching with Redis, pessimistic DB locking for inventory deduction, and JWT role-based access control.",
        system_architecture_mermaid="""graph LR
    User[Client Request] --> Limiter[Redis Token-Bucket Rate Limiter]
    Limiter --> Auth[JWT Auth Middleware]
    Auth --> API[FastAPI Core Router]
    API <-->|Cached Products| Cache[(Redis Cache)]
    API <-->|ACID Transactions| DB[(PostgreSQL Database)]""",
        core_features=[
            "Two-tier caching strategy (Cache-Aside + Write-Through) with automated TTL eviction",
            "ACID-compliant inventory reservation handling concurrent order placements without overselling",
            "Role-Based Access Control (RBAC) with secure JWT refresh token rotations",
            "Comprehensive OpenAPI documentation with automated integration test suites"
        ],
        database_models=["Product (id, title, price, stock_count, category_id)", "Order (id, user_id, total_amount, status, created_at)", "OrderItem (id, order_id, product_id, quantity)"],
        resume_bullet_points=[
            "Architected a high-concurrency e-commerce API with FastAPI, PostgreSQL, and Redis, sustaining 3,500 requests/sec with p95 latency under 20ms.",
            "Eliminated database lock contention using Redis atomic operations and pessimistic row-level DB locks, preventing inventory overselling.",
            "Implemented Cache-Aside pattern with intelligent invalidation, reducing primary PostgreSQL load by 80%."
        ],
        github_starter_topics=["fastapi", "redis", "postgresql", "ecommerce", "system-design"]
    ),
    ProjectTemplate(
        id="crossplatform-mobile-fintech",
        title="Offline-First FinTech Expense Tracker & Budget Analytics App",
        tagline="Cross-platform mobile application with local SQLite synchronization, biometrics, and dynamic interactive spend charts.",
        difficulty="Intermediate",
        estimated_hours=25,
        target_roles=["mobile-engineer", "frontend-engineer", "fullstack-developer"],
        skills_covered=["TypeScript", "React Native", "Responsive Design", "REST APIs", "SQL", "Git"],
        architecture_overview="A native mobile experience for iOS and Android. Features an offline-first architecture using local SQLite storage that seamlessly syncs transactions with a cloud backend when network connectivity is restored.",
        system_architecture_mermaid="""graph TD
    UI[React Native Mobile UI] <--> LocalDB[(Local SQLite Storage)]
    UI --> Sync[Background Sync Engine]
    Sync <-->|Network Online| CloudAPI[Cloud Backend REST API]
    CloudAPI <--> RemoteDB[(PostgreSQL)]""",
        core_features=[
            "Offline-first state synchronization with delta conflict resolution",
            "Biometric authentication (FaceID / Fingerprint) and secure encrypted token storage",
            "Interactive financial visualization charts (SVG/Skia) rendering categorized monthly spending",
            "Automated recurring subscription detectors and budget limit notifications"
        ],
        database_models=["Transaction (id, amount, category, merchant, timestamp, is_synced)", "Budget (id, category, monthly_limit, current_spent)"],
        resume_bullet_points=[
            "Developed an offline-first mobile financial tracker using React Native and SQLite, enabling instant UI interactions with 0ms network latency.",
            "Engineered bidirectional sync reconciliation algorithms to resolve conflicting offline updates upon network reconnect.",
            "Integrated hardware biometrics (Keychain/Keystore) and custom interactive data charts using React Native SVG."
        ],
        github_starter_topics=["react-native", "typescript", "mobile", "sqlite", "fintech"]
    )
]
