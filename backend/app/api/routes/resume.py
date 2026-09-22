import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ...schemas.resume import ParseResumeResponse, ParseTextRequest
from ...services.resume_service import ResumeService
from ...config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/resume", tags=["Resume Parser"])

resume_service = ResumeService()

@router.get("/parser-status")
def get_parser_status():
    """
    Returns the status of the parsing engine and LLM connection.
    """
    is_gemini_active = resume_service.llm_service.is_available()
    return {
        "status": "healthy",
        "llm_provider": "google-gemini" if is_gemini_active else "rule_based_fallback",
        "model": settings.DEFAULT_LLM_MODEL if is_gemini_active else "none",
        "gemini_api_configured": is_gemini_active
    }

@router.post("/parse-file", response_model=ParseResumeResponse)
async def parse_resume_file(file: UploadFile = File(...)):
    """
    Upload a resume file (.pdf, .docx, .txt) and receive structured JSON extraction.
    """
    filename = file.filename or "unknown_resume.pdf"
    lower_name = filename.lower()
    
    if not (lower_name.endswith(".pdf") or lower_name.endswith(".docx") or lower_name.endswith(".doc") or lower_name.endswith(".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file extension. Please upload a PDF, DOCX, or TXT file."
        )

    file_bytes = await file.read()
    
    # Check max file size
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )

    try:
        response = resume_service.parse_file(filename=filename, file_bytes=file_bytes)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error parsing resume: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while parsing the resume.")

@router.post("/parse-text", response_model=ParseResumeResponse)
def parse_resume_text(payload: ParseTextRequest):
    """
    Parse raw resume text directly without file upload. Useful for API testing and manual inputs.
    """
    try:
        return resume_service.parse_raw_text(payload.text)
    except Exception as e:
        logger.error(f"Error parsing resume text: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
