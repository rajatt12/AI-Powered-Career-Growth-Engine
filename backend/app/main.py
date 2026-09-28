import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .api.routes.resume import router as resume_router
from .api.routes.roles import router as roles_router
from .api.routes.projects import router as projects_router
from .api.routes.roadmap import router as roadmap_router
from .api.routes.auth import router as auth_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## 🚀 AI Career Architect & Growth Engine
    Transforms raw resumes into structured insights, role matches, skill gap analyses, and actionable learning roadmaps.
    
    ### Capabilities:
    * **Personalized Authentication:** User registration, login, and saved career progress tracking.
    * **Resume Ingestion & Parsing:** PDF & DOCX text extraction with structured Pydantic schema via Google Gemini.
    * **Role Matching & Embeddings:** ChromaDB vector search + hybrid skill overlap scoring across curated tech role archetypes.
    * **Portfolio Project Recommender:** Content-based recommendation engine suggesting production-grade architectures with Mermaid diagrams and XYZ resume bullet points.
    * **Personalized Roadmap Planner:** RAG-grounded curriculum engine creating time-boxed, week-by-week learning schedules with milestone tracking.
    """
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(roles_router)
app.include_router(projects_router)
app.include_router(roadmap_router)

@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Mount static frontend Single Page Application
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
