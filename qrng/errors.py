"""QRNG API error types."""

from typing import Optional, Dict, Any


class QRNGError(Exception):
    """Base exception for QRNG API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}


class AuthenticationError(QRNGError):
    """Authentication failed (invalid API key)."""
    pass


class RateLimitError(QRNGError):
    """Rate limit exceeded."""
    pass


class QuotaExceededError(QRNGError):
    """Monthly quota exceeded."""
    pass
