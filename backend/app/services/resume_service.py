import logging
from typing import Optional, Tuple
from ..parsers.file_extractor import FileExtractor
from ..parsers.regex_parser import RegexParser
from ..services.llm_service import LLMParserService
from ..schemas.resume import ParsedResumeProfile, ParseResumeResponse

logger = logging.getLogger(__name__)

class ResumeService:
    """
    Core orchestrator that runs the entire parsing pipeline:
    1. Document Text Extraction (PDF/DOCX)
    2. Deterministic Contact & Link Pre-parsing (Regex)
    3. LLM Semantic & Structured Extraction (Gemini / Fallback)
    4. Data Synthesis & Validation
    """

    def __init__(self, llm_service: Optional[LLMParserService] = None):
        self.llm_service = llm_service or LLMParserService()

    def parse_file(self, filename: str, file_bytes: bytes) -> ParseResumeResponse:
        """
        Extracts and parses a resume from raw file bytes.
        """
        warnings = []
        try:
            raw_text, file_type = FileExtractor.extract_text(filename, file_bytes)
        except Exception as e:
            logger.error(f"File extraction error for {filename}: {e}")
            raise ValueError(f"Could not extract text from document: {str(e)}")

        if len(raw_text.strip()) < 50:
            warnings.append("Extracted text is very short. Ensure the document is not an image-only scan.")

        return self._process_text(raw_text, filename=filename, extraction_method=f"hybrid_{file_type}_llm", warnings=warnings)

    def parse_raw_text(self, text: str) -> ParseResumeResponse:
        """
        Parses resume from a raw text string.
        """
        return self._process_text(text, filename="raw_text_input.txt", extraction_method="hybrid_text_llm")

    def _process_text(self, text: str, filename: str, extraction_method: str, warnings: Optional[list] = None) -> ParseResumeResponse:
        warnings = warnings or []

        # 1. Deterministic Pass (Regex)
        pre_contacts = RegexParser.extract_contacts(text)

        # 2. LLM / Semantic Pass
        profile = self.llm_service.parse_resume(raw_text=text, pre_contacts=pre_contacts)

        # 3. Post-processing & Enrichment
        if not profile.contact.email and not pre_contacts.email:
            warnings.append("No email address was detected in the resume.")
        if not profile.skills.languages and not profile.skills.frameworks:
            warnings.append("Few or no technical skills were detected.")

        return ParseResumeResponse(
            success=True,
            filename=filename,
            extraction_method=extraction_method,
            profile=profile,
            warnings=warnings
        )
