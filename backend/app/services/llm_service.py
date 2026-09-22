import json
import logging
from typing import Optional
from google import genai
from google.genai import types
from ..schemas.resume import ParsedResumeProfile, ContactInfo, SkillCategories, WorkExperience, ProjectItem, EducationItem
from ..config import settings

logger = logging.getLogger(__name__)

class LLMParserService:
    """
    Structured extraction service using Google Gemini with strict Pydantic JSON Schema enforcement.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client: {e}")

    def is_available(self) -> bool:
        return self.client is not None and bool(self.api_key)

    def parse_resume(self, raw_text: str, pre_contacts: Optional[ContactInfo] = None) -> ParsedResumeProfile:
        """
        Parses raw resume text into a structured ParsedResumeProfile.
        If Gemini API key is configured, uses Gemini with strict structured output.
        Otherwise, falls back to a deterministic semantic parser.
        """
        if self.is_available():
            return self._parse_with_gemini(raw_text, pre_contacts)
        else:
            logger.info("GEMINI_API_KEY not configured. Using rule-based fallback parser.")
            return self._fallback_rule_based_parse(raw_text, pre_contacts)

    def _parse_with_gemini(self, raw_text: str, pre_contacts: Optional[ContactInfo] = None) -> ParsedResumeProfile:
        """
        Executes structured JSON extraction using Gemini 2.5 Flash with Pydantic response_schema.
        """
        contact_hints = ""
        if pre_contacts:
            contact_hints = f"Pre-extracted contact hints: Email={pre_contacts.email}, Phone={pre_contacts.phone}, LinkedIn={pre_contacts.linkedin_url}, GitHub={pre_contacts.github_url}"

        prompt = f"""
You are a Principal Technical Recruiter and AI Resume Parser.
Analyze the following resume text and extract all information into the strict structured schema.

CRITICAL EXTRACTION GUIDELINES:
1. Extract and categorize ALL technical skills into:
   - languages (e.g. Python, TypeScript, Java, C++)
   - frameworks (e.g. FastAPI, React, Next.js, Django, Node.js)
   - databases_and_storage (e.g. PostgreSQL, Redis, MongoDB, DynamoDB)
   - cloud_and_devops (e.g. AWS, Docker, Kubernetes, CI/CD, Terraform)
   - ai_and_ml (e.g. PyTorch, HuggingFace, LangChain, Sentence-Transformers, RAG)
   - tools_and_platforms (e.g. Git, Linux, Postman)
   - soft_skills (e.g. System Design, Agile, Mentorship)

2. Quantified Impact Extraction:
   - In 'work_experience' and 'projects', actively identify and extract all quantifiable metrics (e.g., 'reduced query latency by 40%', 'handled 50,000 requests/sec', 'saved $15k/month').

3. Estimate total professional experience in years and calculate seniority level accurately.

{contact_hints}

RESUME TEXT:
----------------
{raw_text}
----------------
"""
        try:
            response = self.client.models.generate_content(
                model=settings.DEFAULT_LLM_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ParsedResumeProfile,
                    temperature=0.1,
                ),
            )
            
            # Pydantic validation of LLM output
            parsed_profile = ParsedResumeProfile.model_validate_json(response.text)
            
            # Merge deterministic contact info if LLM missed any
            if pre_contacts:
                if not parsed_profile.contact.email and pre_contacts.email:
                    parsed_profile.contact.email = pre_contacts.email
                if not parsed_profile.contact.phone and pre_contacts.phone:
                    parsed_profile.contact.phone = pre_contacts.phone
                if not parsed_profile.contact.linkedin_url and pre_contacts.linkedin_url:
                    parsed_profile.contact.linkedin_url = pre_contacts.linkedin_url
                if not parsed_profile.contact.github_url and pre_contacts.github_url:
                    parsed_profile.contact.github_url = pre_contacts.github_url

            return parsed_profile

        except Exception as e:
            logger.error(f"Gemini API structured extraction failed: {e}. Falling back to rule-based parser.")
            return self._fallback_rule_based_parse(raw_text, pre_contacts)

    def _fallback_rule_based_parse(self, raw_text: str, pre_contacts: Optional[ContactInfo] = None) -> ParsedResumeProfile:
        """
        Deterministic fallback parser when LLM is offline or no API key is provided.
        Uses keyword taxonomies and section heuristics.
        """
        contact = pre_contacts or ContactInfo()
        lower_text = raw_text.lower()
        
        # Skill taxonomies
        LANGUAGES = ["python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "ruby", "php", "sql", "html", "css", "r", "scala", "swift", "kotlin"]
        FRAMEWORKS = ["fastapi", "flask", "django", "react", "react.js", "next.js", "vue", "angular", "express", "node.js", "spring boot", "tailwind", "pytorch", "tensorflow"]
        DBS = ["postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "dynamodb", "cassandra"]
        DEVOPS = ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "github actions", "terraform", "linux", "nginx", "jenkins"]
        AI_ML = ["pytorch", "tensorflow", "scikit-learn", "huggingface", "langchain", "embeddings", "rag", "nlp", "computer vision", "transformers"]
        TOOLS = ["git", "github", "postman", "jira", "vs code", "bash"]

        found_langs = [l.title() if len(l) > 3 else l.upper() for l in LANGUAGES if l in lower_text]
        found_fw = [f.title() for f in FRAMEWORKS if f in lower_text]
        found_dbs = [d.title() for d in DBS if d in lower_text]
        found_devops = [d.title() if len(d) > 3 else d.upper() for d in DEVOPS if d in lower_text]
        found_aiml = [a.title() for a in AI_ML if a in lower_text]
        found_tools = [t.title() for t in TOOLS if t in lower_text]

        # Extract summary or first paragraph
        paragraphs = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 40]
        summary = paragraphs[0] if paragraphs else "Candidate profile extracted from resume document."

        # Detect quantified metrics with regex
        import re
        metrics_regex = re.compile(r'(\d+%\s*(?:increase|reduction|improvement|faster|growth|decrease)?|\$\d+[\d,]*|\d+\s*(?:ms|seconds|x|million|k|users|requests))', re.IGNORECASE)
        quantified = []
        for line in raw_text.splitlines():
            if metrics_regex.search(line):
                quantified.append(line.strip(" -*•"))

        # Build fallback profile
        return ParsedResumeProfile(
            summary=summary,
            contact=contact,
            skills=SkillCategories(
                languages=list(set(found_langs)),
                frameworks=list(set(found_fw)),
                databases_and_storage=list(set(found_dbs)),
                cloud_and_devops=list(set(found_devops)),
                ai_and_ml=list(set(found_aiml)),
                tools_and_platforms=list(set(found_tools)),
                soft_skills=["Problem Solving", "Collaboration", "Communication"]
            ),
            work_experience=[
                WorkExperience(
                    company="Company Extracted",
                    role="Software Engineer",
                    quantified_impacts=quantified[:5],
                    tech_stack=list(set(found_langs + found_fw))[:6]
                )
            ] if quantified else [],
            projects=[],
            education=[],
            total_experience_years=2.0,
            detected_seniority="Mid-Level" if len(found_langs) > 3 else "Entry-Level"
        )
