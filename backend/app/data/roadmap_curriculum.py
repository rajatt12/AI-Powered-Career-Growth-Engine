from typing import Dict, List
from ..schemas.roadmap import CuratedResource

# Knowledge Base of Curriculum Modules & Learning Nodes
ROLE_CURRICULUM_DATABASE: Dict[str, List[dict]] = {
    "backend-engineer": [
        {
            "topic_slug": "api-architecture-async",
            "skills_targeted": ["FastAPI", "Python", "REST APIs", "Async"],
            "phase": "API Design & Asynchronous Architecture",
            "title": "Production REST API Architecture & Asynchronous Programming",
            "objective": "Master async/await event loops, dependency injection, and clean layering in FastAPI.",
            "key_topics": ["Asynchronous Event Loops", "FastAPI Dependency Injection", "Pydantic V2 Request/Response Validation", "Error Handling & Middleware"],
            "resources": [
                CuratedResource(title="FastAPI Official Tutorial & Architecture Guide", url="https://fastapi.tiangolo.com/tutorial/", resource_type="Documentation"),
                CuratedResource(title="Real Python: Async IO in Python", url="https://realpython.com/async-io-python/", resource_type="Article")
            ],
            "practical_task": "Build a modular REST API with JWT authentication, custom middleware, and OpenAPI documentation.",
            "interview_question": "Explain the difference between synchronous and asynchronous I/O in Python. When would async not improve performance?"
        },
        {
            "topic_slug": "database-indexing-optimization",
            "skills_targeted": ["PostgreSQL", "SQL", "Database Optimization"],
            "phase": "Data Layer & Query Performance",
            "title": "Relational Modeling, Indexing & Query Optimization in PostgreSQL",
            "objective": "Design normalized schemas, analyze query execution plans with EXPLAIN ANALYZE, and build B-Tree/GIN indexes.",
            "key_topics": ["B-Tree & GIN Indexes", "EXPLAIN ANALYZE Cost Breakdown", "Connection Pooling (pgbouncer/SQLAlchemy)", "ACID Transactions & Row Locking"],
            "resources": [
                CuratedResource(title="Use The Index, Luke! (SQL Indexing Guide)", url="https://use-the-index-luke.com/", resource_type="Interactive Tutorial"),
                CuratedResource(title="PostgreSQL Official Documentation: Indexes", url="https://www.postgresql.org/docs/current/indexes.html", resource_type="Documentation")
            ],
            "practical_task": "Analyze a slow query execution plan on a 100,000 row table and optimize it using composite indexes and connection pooling.",
            "interview_question": "What is the difference between a Clustered and Non-Clustered index, and how do you handle deadlocks in relational transactions?"
        },
        {
            "topic_slug": "redis-caching-strategies",
            "skills_targeted": ["Redis", "Caching"],
            "phase": "High-Throughput Caching & Memory",
            "title": "Distributed Caching Strategies & Rate Limiting with Redis",
            "objective": "Implement Cache-Aside, Write-Through, TTL eviction patterns, and token-bucket rate limiters.",
            "key_topics": ["Cache-Aside vs Write-Through Pattern", "Redis Data Structures (Hashes, Sorted Sets)", "Cache Stampede / Thundering Herd Prevention", "Distributed Locking with Redlock"],
            "resources": [
                CuratedResource(title="Redis University: Caching Patterns", url="https://redis.io/university/", resource_type="Documentation"),
                CuratedResource(title="System Design Primer: Caching Patterns", url="https://github.com/donnemartin/system-design-primer#caching", resource_type="GitHub Repo")
            ],
            "practical_task": "Implement a Redis caching layer over PostgreSQL queries with 5-minute TTL and automatic invalidation on record updates.",
            "interview_question": "How do you solve the Cache Penetration, Cache Breakdown (Thundering Herd), and Cache Avalanche problems?"
        },
        {
            "topic_slug": "celery-async-workers",
            "skills_targeted": ["Celery", "Redis", "Background Jobs"],
            "phase": "Asynchronous Task Processing",
            "title": "Distributed Task Queues & Asynchronous Workers with Celery",
            "objective": "Offload long-running computations from the HTTP cycle to scalable worker pools with retry logic.",
            "key_topics": ["Celery Architecture & Brokers", "Task Retries with Exponential Backoff", "Dead Letter Queues (DLQ)", "Worker Concurrency & Prefetching"],
            "resources": [
                CuratedResource(title="Celery First Steps with FastAPI", url="https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html", resource_type="Documentation")
            ],
            "practical_task": "Create a background worker that generates PDF receipts and sends simulated email notifications asynchronously.",
            "interview_question": "What happens if a Celery worker crashes mid-execution? How do you ensure idempotent task processing?"
        },
        {
            "topic_slug": "docker-containerization",
            "skills_targeted": ["Docker", "Containers", "DevOps"],
            "phase": "Containerization & Deployment",
            "title": "Production Containerization with Docker & Multi-Stage Builds",
            "objective": "Package applications into minimal, secure, and reproducible container images.",
            "key_topics": ["Docker Layer Caching", "Multi-Stage Dockerfile Optimization", "Docker Compose Multi-Container Networking", "Non-root Container Security"],
            "resources": [
                CuratedResource(title="Docker Official Docs: Best Practices for Python", url="https://docs.docker.com/language/python/build-images/", resource_type="Documentation")
            ],
            "practical_task": "Write a multi-stage Dockerfile for FastAPI + PostgreSQL + Redis with a total image size under 120MB.",
            "interview_question": "Why should you avoid running containers as root, and how do multi-stage Docker builds reduce image vulnerability surfaces?"
        },
        {
            "topic_slug": "system-design-microservices",
            "skills_targeted": ["System Design", "Microservices", "Scalability"],
            "phase": "System Design & Capstone",
            "title": "Scalable System Design & Production Deployment",
            "objective": "Design resilient distributed systems handling millions of users with load balancers and horizontal scaling.",
            "key_topics": ["Horizontal Scaling & Load Balancing", "CAP Theorem & Eventual Consistency", "Database Sharding & Replication", "API Gateway & Circuit Breaker Pattern"],
            "resources": [
                CuratedResource(title="System Design Primer by Donne Martin", url="https://github.com/donnemartin/system-design-primer", resource_type="GitHub Repo")
            ],
            "practical_task": "Complete your Capstone Project: Deploy your Distributed Task Processing Engine or High-Concurrency API with full documentation.",
            "interview_question": "How would you design a URL shortener like bit.ly or a distributed rate limiter to handle 10,000 requests per second?"
        }
    ],
    "ai-ml-engineer": [
        {
            "topic_slug": "deep-learning-pytorch",
            "skills_targeted": ["Python", "PyTorch", "Deep Learning"],
            "phase": "Deep Learning & Neural Foundations",
            "title": "PyTorch Tensor Operations, Autograd & Custom Neural Architectures",
            "objective": "Build and train custom neural networks from scratch using PyTorch tensors and gradient descent.",
            "key_topics": ["Tensor Manipulation & GPU Acceleration (CUDA)", "Autograd Mechanics & Loss Functions", "Custom Datasets & DataLoaders", "Model Evaluation Benchmarks"],
            "resources": [
                CuratedResource(title="Deep Learning with PyTorch: A 60 Minute Blitz", url="https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html", resource_type="Documentation")
            ],
            "practical_task": "Train a multi-layer neural network on a tabular dataset with custom training loops, learning rate schedulers, and early stopping.",
            "interview_question": "Explain how backpropagation and the chain rule calculate gradients in PyTorch autograd."
        },
        {
            "topic_slug": "transformers-huggingface",
            "skills_targeted": ["HuggingFace", "Transformers", "NLP"],
            "phase": "Transformer Architectures & NLP",
            "title": "Transformer Mechanics, Self-Attention & Hugging Face Ecosystem",
            "objective": "Understand multi-head attention and fine-tune pretrained transformer models for classification and extraction.",
            "key_topics": ["Self-Attention & Positional Encodings", "Hugging Face AutoModel & Tokenizers", "LoRA / QLoRA Parameter-Efficient Fine-Tuning", "Perplexity & BLEU/ROUGE Evaluation"],
            "resources": [
                CuratedResource(title="Hugging Face NLP Course", url="https://huggingface.co/learn/nlp-course", resource_type="Interactive Tutorial")
            ],
            "practical_task": "Fine-tune a lightweight BERT or DistilBERT model for technical resume text categorization using the Hugging Face Trainer API.",
            "interview_question": "Why did Multi-Head Attention replace RNNs and LSTMs for natural language processing tasks?"
        },
        {
            "topic_slug": "rag-vector-databases",
            "skills_targeted": ["RAG", "ChromaDB", "Embeddings", "Vector Databases"],
            "phase": "Retrieval-Augmented Generation & Vector Search",
            "title": "Vector Embeddings, ChromaDB Indexing & Production RAG Pipelines",
            "objective": "Build end-to-end RAG systems with recursive chunking, dense vector retrieval, and hallucination guardrails.",
            "key_topics": ["Dense vs Sparse Embeddings", "ChromaDB / FAISS HNSW Indexing", "Contextual Reranking & Hybrid Search", "Prompt Grounding & Citation Verification"],
            "resources": [
                CuratedResource(title="ChromaDB Official Documentation", url="https://docs.trychroma.com/", resource_type="Documentation")
            ],
            "practical_task": "Implement a full RAG pipeline that ingests technical PDFs and answers technical questions with exact paragraph citations.",
            "interview_question": "How do you evaluate RAG retrieval quality using metrics like Hit Rate, MRR, and Context Relevance?"
        },
        {
            "topic_slug": "ml-deployment-fastapi",
            "skills_targeted": ["FastAPI", "Docker", "Model Serving"],
            "phase": "Model Deployment & Capstone",
            "title": "High-Performance Model Serving & Production Capstone",
            "objective": "Wrap PyTorch/Transformer models in asynchronous FastAPI endpoints with batching, ONNX optimization, and Docker.",
            "key_topics": ["ONNX Runtime & TensorRT Optimization", "Dynamic Batching for Inference", "Docker Containerization for ML Services", "Latency & Memory Profiling"],
            "resources": [
                CuratedResource(title="FastAPI for Machine Learning Deployment", url="https://fastapi.tiangolo.com/", resource_type="Documentation")
            ],
            "practical_task": "Complete your Capstone Project: Deploy the Enterprise RAG Agent or MLOps Retraining Pipeline with sub-100ms inference.",
            "interview_question": "How do you optimize an LLM or PyTorch model for production inference to minimize latency and GPU memory footprint?"
        }
    ],
    "fullstack-developer": [
        {
            "topic_slug": "modern-react-typescript",
            "skills_targeted": ["React", "TypeScript", "Frontend"],
            "phase": "Modern React & Component Architecture",
            "title": "Component Architecture, TypeScript & State Management in React",
            "objective": "Build type-safe frontend components with custom hooks and responsive glassmorphic interfaces.",
            "key_topics": ["React 18 Concurrent Rendering", "TypeScript Generics & Component Props", "Zustand / Context State Management", "Tailwind CSS & Glassmorphism Design"],
            "resources": [
                CuratedResource(title="React Official Documentation", url="https://react.dev/", resource_type="Documentation"),
                CuratedResource(title="TypeScript for React Developers", url="https://www.typescriptlang.org/docs/handbook/react.html", resource_type="Documentation")
            ],
            "practical_task": "Build an interactive dynamic dashboard with dark mode, responsive sidebar, and custom TypeScript state hooks.",
            "interview_question": "Explain the React reconciliation algorithm and how the Virtual DOM minimizes direct browser DOM manipulation."
        },
        {
            "topic_slug": "fullstack-api-integration",
            "skills_targeted": ["FastAPI", "Node.js", "PostgreSQL", "Full-Stack"],
            "phase": "Full-Stack API Integration & Security",
            "title": "Secure API Integration, JWT Auth & Database Relationships",
            "objective": "Connect reactive frontends to relational backend APIs with robust authentication and optimistic updates.",
            "key_topics": ["Axios / Fetch Interceptors", "JWT Refresh Token Strategy", "Optimistic UI Updates", "CORS Configuration & Security Headers"],
            "resources": [
                CuratedResource(title="FastAPI Security & OAuth2", url="https://fastapi.tiangolo.com/tutorial/security/", resource_type="Documentation")
            ],
            "practical_task": "Build end-to-end user authentication with JWT token storage in HttpOnly cookies and protected dashboard routes.",
            "interview_question": "How do you prevent Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) in full-stack web applications?"
        },
        {
            "topic_slug": "websockets-realtime-fullstack",
            "skills_targeted": ["WebSockets", "Redis", "Real-Time"],
            "phase": "Real-Time Collaboration & Deployment",
            "title": "Real-Time WebSockets & Full-Stack Cloud Deployment",
            "objective": "Implement bidirectional WebSocket streams, Redis Pub/Sub syncing, and deploy full-stack apps.",
            "key_topics": ["Bidirectional WebSocket Channels", "Redis Pub/Sub Multi-Instance Sync", "Vercel / Docker Cloud Deployments", "CI/CD Deployment Pipelines"],
            "resources": [
                CuratedResource(title="WebSocket API Documentation (MDN)", url="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API", resource_type="Documentation")
            ],
            "practical_task": "Complete your Capstone Project: Deploy the Real-Time Collaborative Workspace or E-Commerce Platform.",
            "interview_question": "What are the trade-offs between WebSockets, Server-Sent Events (SSE), and Short/Long Polling?"
        }
    ]
}
