from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes.resume import router as resume_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## 🚀 AI Career Architect & Resume Intelligence Engine
    Transforms raw resumes into structured insights, role matches, skill gap analyses, and actionable learning roadmaps.
    
    ### Phase 1 Features:
    * **File Ingestion:** PDF & DOCX text parsing with layout preservation.
    * **Deterministic Heuristics:** Regex extraction for contacts & profiles.
    * **Structured LLM Parsing:** Pydantic schema-guided entity extraction via Google Gemini.
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
