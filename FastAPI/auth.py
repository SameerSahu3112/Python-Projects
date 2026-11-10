"""
Apple Store — Security & Authentication Utilities
Handles password hashing, session management, and auth dependencies.
"""
import hashlib
import secrets
import os
from datetime import datetime, timedelta
from functools import wraps

# Try bcrypt first, fallback to SHA-256 if unavailable
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


# ─── Password Hashing ─────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt (preferred) or SHA-256 fallback."""
    if BCRYPT_AVAILABLE:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    else:
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"sha256${salt}${hashed}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    if BCRYPT_AVAILABLE and password_hash.startswith("$2"):
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    elif password_hash.startswith("sha256$"):
        parts = password_hash.split("$")
        if len(parts) != 3:
            return False
        _, salt, stored_hash = parts
        computed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return secrets.compare_digest(computed, stored_hash)
    return False


# ─── Session Token Generation ─────────────────────────────────

def generate_session_token() -> str:
    """Generate a cryptographically secure session token."""
    return secrets.token_urlsafe(48)


# ─── Order Number Generation ──────────────────────────────────

def generate_order_number() -> str:
    """Generate a unique order number like APL-20261110-XXXXX."""
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    random_part = secrets.token_hex(3).upper()[:5]
    return f"APL-{date_part}-{random_part}"
