"""QRNG API REST client."""

import requests
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass

from .errors import QRNGError, AuthenticationError, RateLimitError, QuotaExceededError


FormatType = Literal["hex", "base64", "binary", "uint8", "uint32"]
MethodType = Literal["auto", "photon", "tunneling", "vacuum", "simulator"]
SignatureType = Literal["ed25519", "dilithium2", "dilithium3", "dilithium5"]


@dataclass
class EntropyResult:
    """Result from entropy generation."""
    
    data: str
    proof_id: str
    signature: str
    public_key: str
    signature_type: str
    metadata: Dict[str, Any]
    
    def verify(self) -> bool:
        """Verify the cryptographic signature (requires verification libraries)."""
        # Implementation note: Users should install verification libraries
        # ed25519: python-ed25519 or cryptography
        # dilithium: use @noble/post-quantum via subprocess or FFI
        raise NotImplementedError(
            "Signature verification requires installing additional libraries. "
            "See documentation for Ed25519 and Dilithium verification."
        )


@dataclass
class HealthStatus:
    """System health metrics."""
    
    status: str
    metrics: Dict[str, Any]
    timestamp: str


class QRNGClient:
    """
    QRNG API REST client.
    
    Example:
        >>> client = QRNGClient(api_key="qnrk_...")
        >>> result = client.generate(bytes=32, format="hex")
        >>> print(result.data)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://qrngapi.com",
        timeout: int = 30
    ):
        """
        Initialize QRNG client.
        
        Args:
            api_key: Your QRNG API key
            base_url: API base URL (default: https://qrngapi.com)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})
    
    def generate(
        self,
        bytes: int = 32,
        format: FormatType = "hex",
        method: Optional[MethodType] = None,
        signature_type: Optional[SignatureType] = None,
    ) -> EntropyResult:
        """
        Generate random entropy.
        
        Args:
            bytes: Number of random bytes to generate (1-1024)
            format: Output format (hex, base64, binary, uint8, uint32)
            method: Quantum method (auto, photon, tunneling, vacuum, simulator)
            signature_type: Signature type (ed25519, dilithium2, dilithium3, dilithium5)
                           PQC signatures require Pro tier or higher
        
        Returns:
            EntropyResult with random data and cryptographic proof
        
        Raises:
            AuthenticationError: Invalid API key
            RateLimitError: Rate limit exceeded
            QuotaExceededError: Monthly quota exceeded
            QRNGError: Other API errors
        """
        params = {
            "bytes": bytes,
            "format": format,
        }
        
        if method:
            params["method"] = method
        if signature_type:
            params["signatureType"] = signature_type
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/random",
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code == 402:
                raise QuotaExceededError("Monthly quota exceeded")
            elif not response.ok:
                data = response.json() if response.headers.get("content-type") == "application/json" else {}
                raise QRNGError(
                    data.get("error", f"HTTP {response.status_code}"),
                    status_code=response.status_code,
                    response=data
                )
            
            data = response.json()
            
            return EntropyResult(
                data=data["data"],
                proof_id=data["proofId"],
                signature=data["signature"],
                public_key=data["publicKey"],
                signature_type=data["signatureType"],
                metadata=data.get("metadata", {})
            )
            
        except requests.exceptions.RequestException as e:
            raise QRNGError(f"Request failed: {e}")
    
    def health(self) -> HealthStatus:
        """
        Get system health status.
        
        Returns:
            HealthStatus with NIST test results
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return HealthStatus(
                status=data["status"],
                metrics=data["metrics"],
                timestamp=data["timestamp"]
            )
            
        except requests.exceptions.RequestException as e:
            raise QRNGError(f"Health check failed: {e}")
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
