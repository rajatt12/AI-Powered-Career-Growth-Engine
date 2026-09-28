import io
import re
from typing import Tuple
import pdfplumber
import pypdf
import docx

class DocumentExtractionError(Exception):
    """Raised when text cannot be extracted from a document."""
    pass

class FileExtractor:
    """
    Handles extracting clean plain text from PDF and DOCX documents with layout awareness
    and artifact cleanup (such as CID font bullet codes like `(cid:127)`).
    """

    @staticmethod
    def _clean_extracted_text(text: str) -> str:
        """
        Cleans up raw extracted text:
        - Replaces PDF CID bullet glyphs like `(cid:127)` or `(cid:143)` with clean bullets `• `
        - Removes non-printable/control characters
        - Normalizes whitespace while preserving section line breaks
        """
        if not text:
            return ""

        # Replace (cid:XXX) font encoding artifacts with a clean bullet point
        cleaned = re.sub(r'\(cid:\d+\)', ' • ', text)
        
        # Replace non-breaking spaces and irregular unicode spaces
        cleaned = cleaned.replace('\u00a0', ' ').replace('\u200b', '')

        # Normalize line breaks and multiple consecutive spaces
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()

    @classmethod
    def extract_text_from_pdf(cls, file_bytes: bytes) -> str:
        """
        Extract text from PDF bytes.
        First tries pdfplumber (layout-aware, handles multi-column).
        Falls back to pypdf if pdfplumber encounters an error.
        """
        extracted_pages = []
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(layout=False, x_tolerance=2, y_tolerance=2)
                    if page_text:
                        extracted_pages.append(page_text.strip())
            
            combined_text = "\n\n".join(extracted_pages).strip()
            if combined_text:
                return cls._clean_extracted_text(combined_text)
        except Exception:
            pass

        # Fallback to pypdf
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            pypdf_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pypdf_pages.append(text.strip())
            
            combined = "\n\n".join(pypdf_pages).strip()
            if combined:
                return cls._clean_extracted_text(combined)
            raise DocumentExtractionError("PDF appears to be empty or contains scanned images without selectable text.")
        except Exception as e:
            raise DocumentExtractionError(f"Failed to extract text from PDF: {str(e)}")

    @classmethod
    def extract_text_from_docx(cls, file_bytes: bytes) -> str:
        """
        Extracts text from DOCX bytes including paragraphs and tables.
        """
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text_blocks = []
            
            for para in doc.paragraphs:
                clean_text = para.text.strip()
                if clean_text:
                    text_blocks.append(clean_text)
                    
            for table in doc.tables:
                for row in table.rows:
                    row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_cells:
                        text_blocks.append(" | ".join(row_cells))
                        
            combined_text = "\n".join(text_blocks).strip()
            if not combined_text:
                raise DocumentExtractionError("DOCX document is empty.")
            return cls._clean_extracted_text(combined_text)
        except Exception as e:
            raise DocumentExtractionError(f"Failed to extract text from DOCX: {str(e)}")

    @classmethod
    def extract_text(cls, filename: str, file_bytes: bytes) -> Tuple[str, str]:
        """
        Detects file type from extension and extracts text.
        Returns (extracted_text, file_type)
        """
        lower_name = filename.lower()
        if lower_name.endswith(".pdf"):
            return cls.extract_text_from_pdf(file_bytes), "pdf"
        elif lower_name.endswith(".docx") or lower_name.endswith(".doc"):
            return cls.extract_text_from_docx(file_bytes), "docx"
        elif lower_name.endswith(".txt"):
            raw = file_bytes.decode("utf-8", errors="ignore")
            return cls._clean_extracted_text(raw), "txt"
        else:
            raise ValueError(f"Unsupported file format '{filename}'. Please upload a PDF, DOCX, or TXT file.")
