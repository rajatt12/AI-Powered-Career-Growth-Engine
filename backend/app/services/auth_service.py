import bcrypt
import jwt
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple
from ..database import get_db_connection

logger = logging.getLogger(__name__)

SECRET_KEY = "careerforge-super-secret-jwt-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

class AuthService:
    """Handles User Registration, Password Verification, JWT Tokens, and State Persistence."""

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except Exception:
            return None

    @classmethod
    def register_user(cls, email: str, password: str, full_name: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email_clean = email.strip().lower()
        if not email_clean or len(password) < 4:
            return False, "Invalid email or password (min 4 chars required).", None

        hashed = cls.hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, hashed_password, full_name) VALUES (?, ?, ?)",
                (email_clean, hashed, full_name.strip())
            )
            user_id = cursor.lastrowid
            
            # Initialize empty user state
            cursor.execute(
                "INSERT INTO user_states (user_id, completed_weeks_json) VALUES (?, '[]')",
                (user_id,)
            )
            
            conn.commit()
            token = cls.create_access_token(user_id, email_clean)
            return True, "User registered successfully.", {
                "user_id": user_id,
                "email": email_clean,
                "full_name": full_name.strip(),
                "token": token
            }
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "An account with this email already exists.", None
            return False, f"Registration failed: {str(e)}", None
        finally:
            conn.close()

    @classmethod
    def authenticate_user(cls, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email_clean = email.strip().lower()
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
            user = cursor.fetchone()
            if not user:
                return False, "Invalid email or password.", None

            if not cls.verify_password(password, user["hashed_password"]):
                return False, "Invalid email or password.", None

            token = cls.create_access_token(user["id"], user["email"])
            
            # Fetch user state
            cursor.execute("SELECT * FROM user_states WHERE user_id = ?", (user["id"],))
            state = cursor.fetchone()

            profile = json.loads(state["profile_json"]) if state and state["profile_json"] else None
            roadmap = json.loads(state["roadmap_json"]) if state and state["roadmap_json"] else None
            completed_weeks = json.loads(state["completed_weeks_json"]) if state and state["completed_weeks_json"] else []
            target_role_id = state["target_role_id"] if state else None

            return True, "Login successful.", {
                "user_id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "token": token,
                "state": {
                    "profile": profile,
                    "target_role_id": target_role_id,
                    "roadmap": roadmap,
                    "completed_weeks": completed_weeks
                }
            }
        finally:
            conn.close()

    @classmethod
    def get_user_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, email, full_name, created_at FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if not user:
                return None

            cursor.execute("SELECT * FROM user_states WHERE user_id = ?", (user_id,))
            state = cursor.fetchone()

            profile = json.loads(state["profile_json"]) if state and state["profile_json"] else None
            roadmap = json.loads(state["roadmap_json"]) if state and state["roadmap_json"] else None
            completed_weeks = json.loads(state["completed_weeks_json"]) if state and state["completed_weeks_json"] else []
            target_role_id = state["target_role_id"] if state else None

            return {
                "user_id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "created_at": user["created_at"],
                "state": {
                    "profile": profile,
                    "target_role_id": target_role_id,
                    "roadmap": roadmap,
                    "completed_weeks": completed_weeks
                }
            }
        finally:
            conn.close()

    @classmethod
    def save_user_state(
        cls, 
        user_id: int, 
        profile: Optional[Dict[str, Any]] = None,
        target_role_id: Optional[str] = None,
        roadmap: Optional[Dict[str, Any]] = None,
        completed_weeks: Optional[list] = None
    ) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM user_states WHERE user_id = ?", (user_id,))
            existing = cursor.fetchone()

            p_json = json.dumps(profile) if profile is not None else (existing["profile_json"] if existing else None)
            r_id = target_role_id if target_role_id is not None else (existing["target_role_id"] if existing else None)
            road_json = json.dumps(roadmap) if roadmap is not None else (existing["roadmap_json"] if existing else None)
            w_json = json.dumps(completed_weeks) if completed_weeks is not None else (existing["completed_weeks_json"] if existing else "[]")

            if existing:
                cursor.execute("""
                UPDATE user_states 
                SET profile_json = ?, target_role_id = ?, roadmap_json = ?, completed_weeks_json = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """, (p_json, r_id, road_json, w_json, user_id))
            else:
                cursor.execute("""
                INSERT INTO user_states (user_id, profile_json, target_role_id, roadmap_json, completed_weeks_json)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, p_json, r_id, road_json, w_json))

            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving user state: {e}")
            return False
        finally:
            conn.close()
