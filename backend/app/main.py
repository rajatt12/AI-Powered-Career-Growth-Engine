from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes.resume import router as resume_router
from .api.routes.roles import router as roles_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## 🚀 AI Career Architect & Growth Engine
    Transforms raw resumes into structured insights, role matches, skill gap analyses, and actionable learning roadmaps.
    
    ### Core Capabilities:
    * **Phase 1: Resume Ingestion & Parsing:** PDF & DOCX text extraction with structured Pydantic schema via Google Gemini.
    * **Phase 2: Role Matching & Embeddings:** ChromaDB vector search + hybrid skill overlap scoring across curated tech role archetypes.
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
app.include_router(resume_router)
app.include_router(roles_router)

@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
