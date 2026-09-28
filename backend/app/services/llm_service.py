import json
import logging
import re
from typing import Optional
from google import genai
from google.genai import types
from ..schemas.resume import ParsedResumeProfile, ContactInfo, SkillCategories, WorkExperience, ProjectItem, EducationItem
from ..config import settings

logger = logging.getLogger(__name__)

class LLMParserService:
    """
    Structured extraction service using Google Gemini with strict Pydantic JSON Schema enforcement
    and an intelligent deterministic semantic fallback engine.
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
            logger.info("Using rule-based semantic parser.")
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
1. 'summary': MUST be a concise 2-sentence executive summary (maximum 40 words) describing the candidate's core domain and top strengths. NEVER dump raw unparsed text or whole sections into the summary.
2. Extract and categorize ALL technical skills into:
   - languages (e.g. Python, TypeScript, Java, C++, SQL)
   - frameworks (e.g. FastAPI, React, Next.js, Django, Node.js, Streamlit)
   - databases_and_storage (e.g. PostgreSQL, Redis, MySQL, ChromaDB, FAISS, MongoDB)
   - cloud_and_devops (e.g. AWS, Docker, Kubernetes, CI/CD, Git)
   - ai_and_ml (e.g. PyTorch, HuggingFace, LangChain, Sentence-Transformers, RAG, Embeddings, Pandas, NumPy, Scikit-learn, OpenCV)
   - tools_and_platforms (e.g. Power BI, Tableau, Salesforce, Git, Linux, Postman)
   - soft_skills (e.g. System Design, Agile, Business Analysis, Mentorship)

3. In 'work_experience' and 'projects', extract quantifiable metrics (e.g., 'improved retrieval accuracy by 22%', 'reduced latency by 18%').

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
            
            parsed_profile = ParsedResumeProfile.model_validate_json(response.text)
            
            # Post-process summary length guardrail
            if len(parsed_profile.summary.split()) > 60:
                sentences = re.split(r'(?<=[.!?])\s+', parsed_profile.summary)
                parsed_profile.summary = " ".join(sentences[:2])

            # Merge deterministic contact info if needed
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
        Synthesizes a clean executive summary and extracts skills using curated taxonomies.
        """
        contact = pre_contacts or ContactInfo()
        lower_text = raw_text.lower()
        
        # Skill taxonomies
        LANGUAGES = ["python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "ruby", "php", "sql", "html", "css", "r", "scala"]
        FRAMEWORKS = ["fastapi", "flask", "django", "react", "react.js", "next.js", "vue", "angular", "express", "node.js", "spring boot", "streamlit", "tailwind"]
        DBS = ["postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "dynamodb", "chromadb", "faiss", "qdrant", "pinecone"]
        DEVOPS = ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "github actions", "terraform", "linux", "nginx", "git"]
        AI_ML = ["pytorch", "tensorflow", "scikit-learn", "huggingface", "langchain", "embeddings", "rag", "nlp", "pandas", "numpy", "matplotlib", "seaborn", "opencv", "transformers", "llm", "llms", "prompt engineering"]
        TOOLS = ["power bi", "tableau", "salesforce", "salesforce administration", "postman", "jira", "vs code", "jupyter"]

        def match_skills(vocab_list):
            matched = []
            for item in vocab_list:
                # Word boundary search
                pattern = r'\b' + re.escape(item) + r'\b'
                if re.search(pattern, lower_text):
                    if len(item) <= 3:
                        matched.append(item.upper())
                    else:
                        matched.append(item.title())
            return list(set(matched))

        found_langs = match_skills(LANGUAGES)
        found_fw = match_skills(FRAMEWORKS)
        found_dbs = match_skills(DBS)
        found_devops = match_skills(DEVOPS)
        found_aiml = match_skills(AI_ML)
        found_tools = match_skills(TOOLS)

        # 1. Clean Summary Extraction (NEVER dump raw text)
        summary = ""
        # Search for explicit summary/objective header in text
        summary_match = re.search(
            r'(?:summary|objective|profile|about\s+me)\s*[:\-\n]+\s*(.+?)(?=(?:experience|skills|education|projects|internship|\n\n[A-Z]))',
            raw_text,
            re.IGNORECASE | re.DOTALL
        )
        if summary_match:
            candidate_raw_sum = summary_match.group(1).strip()
            # Take only the first 2 sentences
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', candidate_raw_sum) if len(s.strip()) > 10]
            if sentences:
                summary = " ".join(sentences[:2])

        # If not found or too messy, synthesize a professional executive summary
        if not summary or len(summary) < 20 or len(summary.split()) > 50:
            top_areas = []
            if found_aiml: top_areas.append("AI/ML and Data Analytics")
            if found_langs: top_areas.append(f"{', '.join(found_langs[:3])}")
            if found_dbs: top_areas.append(f"{found_dbs[0]}")
            
            domain_label = "AI/ML Engineer & Data Analyst" if found_aiml else "Software Engineer"
            summary = f"Results-driven {domain_label} with hands-on experience in {' and '.join(top_areas[:2]) if top_areas else 'software development'}. Skilled in building scalable applications, data pipelines, and analytics solutions."

        # 2. Extract Quantified Metrics
        metrics_regex = re.compile(
            r'(\b\d+%\s*(?:increase|reduction|improvement|faster|growth|decrease|accuracy|latency)?|\$\d+[\d,]*|\b\d+\+?\s*(?:ms|seconds|x|million|k|users|requests|documents|workflows|dashboards)\b)', 
            re.IGNORECASE
        )
        quantified = []
        for line in raw_text.splitlines():
            line_clean = line.strip(" -*•\t")
            if len(line_clean) > 20 and metrics_regex.search(line_clean):
                quantified.append(line_clean)

        # 3. Detect Seniority and Years
        total_years = 1.0
        if "intern" in lower_text or "trainee" in lower_text:
            detected_seniority = "Entry-Level"
            total_years = 1.5
        elif "senior" in lower_text:
            detected_seniority = "Senior"
            total_years = 5.0
        else:
            detected_seniority = "Mid-Level" if len(found_langs) >= 3 else "Entry-Level"
            total_years = 2.0

        return ParsedResumeProfile(
            summary=summary,
            contact=contact,
            skills=SkillCategories(
                languages=found_langs,
                frameworks=found_fw,
                databases_and_storage=found_dbs,
                cloud_and_devops=found_devops,
                ai_and_ml=found_aiml,
                tools_and_platforms=found_tools,
                soft_skills=["Data Analysis", "Problem Solving", "Collaboration"]
            ),
            work_experience=[
                WorkExperience(
                    company="Recent Experience",
                    role=detected_seniority + " Engineer",
                    quantified_impacts=quantified[:4],
                    tech_stack=(found_langs + found_fw + found_aiml)[:5]
                )
            ] if quantified else [],
            projects=[],
            education=[],
            total_experience_years=total_years,
            detected_seniority=detected_seniority
        )
