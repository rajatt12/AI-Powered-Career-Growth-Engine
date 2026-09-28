import re
from typing import Dict, List, Optional
from ..schemas.resume import ContactInfo

class RegexParser:
    """
    Deterministic rule-based extractor for contact information, links, and candidate identity.
    """

    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    PHONE_REGEX = re.compile(
        r'(?:(?:\+?(\d{1,3}))?[-.\s]?)?(?:\(?(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})\b'
    )
    LINKEDIN_REGEX = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)/?', re.IGNORECASE)
    GITHUB_REGEX = re.compile(r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/?', re.IGNORECASE)
    URL_REGEX = re.compile(r'https?://[^\s/$.?#].[^\s]*', re.IGNORECASE)

    # Keywords that indicate a line is a COMPANY, institution, or document title (NOT a person's name)
    NON_NAME_KEYWORDS = {
        "pvt", "ltd", "private", "limited", "inc", "corp", "corporation", "llc", 
        "technologies", "digital", "solutions", "services", "labs", "systems", 
        "university", "institute", "college", "school", "academy", "curriculum", 
        "vitae", "resume", "page", "internship", "trainee", "training", "experience",
        "academic", "education", "projects", "skills", "summary"
    }

    @classmethod
    def _is_valid_human_name(cls, line: str) -> bool:
        """Verifies whether a text line looks like a human personal name."""
        clean = line.strip(" |,-•\t")
        words = clean.split()
        
        # Human names are typically 1 to 4 words
        if not (1 <= len(words) <= 4):
            return False

        # Reject if contains email, URL, or digits
        if cls.EMAIL_REGEX.search(clean) or cls.URL_REGEX.search(clean) or any(char.isdigit() for char in clean):
            return False

        # Reject if contains any corporate or document keywords
        lower_words = {w.lower().strip(".,;:()") for w in words}
        if any(keyword in lower_words for keyword in cls.NON_NAME_KEYWORDS):
            return False

        # Check that characters are primarily alphabetic
        if not all(w.replace(".", "").replace("-", "").isalpha() for w in words):
            return False

        return True

    @classmethod
    def extract_contacts(cls, text: str) -> ContactInfo:
        """
        Extract email, phone, LinkedIn, GitHub, and candidate name deterministically.
        """
        email_match = cls.EMAIL_REGEX.search(text)
        email = email_match.group(0) if email_match else None

        phone = None
        for line in text.splitlines()[:15]:
            phone_match = cls.PHONE_REGEX.search(line)
            if phone_match:
                digits = re.sub(r'\D', '', phone_match.group(0))
                if len(digits) >= 10:
                    phone = phone_match.group(0).strip()
                    break

        linkedin_match = cls.LINKEDIN_REGEX.search(text)
        linkedin_url = f"https://linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else None

        github_match = cls.GITHUB_REGEX.search(text)
        github_url = f"https://github.com/{github_match.group(1)}" if github_match else None

        # Robust Candidate Name Extraction
        name = None
        for line in text.splitlines()[:10]:
            clean_line = line.strip(" |,-•\t")
            if not clean_line:
                continue

            # If line contains email/pipe delimiters, extract the first segment
            if "|" in clean_line:
                first_seg = clean_line.split("|")[0].strip()
                if cls._is_valid_human_name(first_seg):
                    name = first_seg.title() if first_seg.isupper() else first_seg
                    break

            if cls._is_valid_human_name(clean_line):
                name = clean_line.title() if clean_line.isupper() else clean_line
                break

        # Fallback to email username if no name found
        if not name and email:
            uname = email.split("@")[0]
            clean_uname = re.sub(r'\d+', '', uname).replace(".", " ").replace("_", " ").strip()
            if len(clean_uname) >= 3:
                name = clean_uname.title()

        return ContactInfo(
            name=name,
            email=email,
            phone=phone,
            linkedin_url=linkedin_url,
            github_url=github_url
        )
