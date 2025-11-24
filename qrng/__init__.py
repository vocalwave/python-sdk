"""
QRNG API Python SDK

Official Python client for the QRNG API - Quantum Random Number Generation as a Service.
"""

from .client import QRNGClient, EntropyResult, HealthStatus
from .errors import QRNGError, AuthenticationError, RateLimitError, QuotaExceededError
from .streaming import QRNGStreamClient

__version__ = "1.0.0"
__all__ = [
    "QRNGClient",
    "QRNGStreamClient",
    "EntropyResult",
    "HealthStatus",
    "QRNGError",
    "AuthenticationError",
    "RateLimitError",
    "QuotaExceededError",
]
