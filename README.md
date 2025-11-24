# QRNG API - Python SDK

Official Python client library for the QRNG API - Quantum Random Number Generation as a Service.

## Installation

```bash
pip install qrng-api
```

## Quick Start

```python
from qrng import QRNGClient

# Initialize client
client = QRNGClient(api_key="your-api-key")

# Generate 32 bytes of quantum random data
result = client.generate(bytes=32, format="hex")
print(f"Random data: {result.data}")
print(f"Proof ID: {result.proof_id}")
print(f"Signature: {result.signature_type}")

# Check system health
health = client.health()
print(f"Status: {health.status}")
```

## Features

- ✅ **REST API**: Full support for random entropy generation
- ✅ **WebSocket Streaming**: Real-time entropy streaming
- ✅ **Post-Quantum Cryptography**: Dilithium signatures (Pro/Enterprise)
- ✅ **Type Safety**: Full type hints and autocomplete
- ✅ **Error Handling**: Comprehensive exception types
- ✅ **Context Manager**: Automatic resource cleanup

## Usage

### Basic Generation

```python
from qrng import QRNGClient

client = QRNGClient(api_key="qnrk_...")

# Generate random hex string
result = client.generate(bytes=32, format="hex")

# Generate base64 encoded data
result = client.generate(bytes=64, format="base64")

# Generate uint8 array
result = client.generate(bytes=16, format="uint8")
```

### Quantum Methods

```python
# Use specific quantum method (requires appropriate tier)
result = client.generate(
    bytes=32,
    format="hex",
    method="photon"  # photon, tunneling, vacuum, simulator
)
```

### Post-Quantum Cryptography

```python
# Pro tier: Dilithium2 signatures
result = client.generate(
    bytes=32,
    signature_type="dilithium2"
)

# Enterprise tier: Advanced Dilithium3/5
result = client.generate(
    bytes=32,
    signature_type="dilithium3"  # or dilithium5
)
```

### WebSocket Streaming

```python
from qrng import QRNGStreamClient

def handle_data(data):
    print(f"Received chunk: {data}")

def handle_error(error):
    print(f"Error: {error}")

# Stream entropy in real-time
stream = QRNGStreamClient(api_key="qnrk_...")
stream.connect(
    on_data=handle_data,
    on_error=handle_error,
    chunk_size=32,
    format="hex"
)

# ... stream runs continuously ...
stream.disconnect()
```

### Context Manager

```python
with QRNGClient(api_key="qnrk_...") as client:
    result = client.generate(bytes=32)
    print(result.data)
# Session automatically closed
```

## API Reference

### QRNGClient

#### `__init__(api_key, base_url="https://qrngapi.com", timeout=30)`

Initialize the client.

**Parameters:**
- `api_key` (str): Your QRNG API key
- `base_url` (str): API base URL
- `timeout` (int): Request timeout in seconds

#### `generate(bytes=32, format="hex", method=None, signature_type=None)`

Generate random entropy.

**Parameters:**
- `bytes` (int): Number of bytes to generate (1-1024)
- `format` (str): Output format - `"hex"`, `"base64"`, `"binary"`, `"uint8"`, `"uint32"`
- `method` (str, optional): Quantum method - `"auto"`, `"photon"`, `"tunneling"`, `"vacuum"`, `"simulator"`
- `signature_type` (str, optional): Signature type - `"ed25519"`, `"dilithium2"`, `"dilithium3"`, `"dilithium5"`

**Returns:** `EntropyResult` with:
- `data`: Random data in requested format
- `proof_id`: Unique proof identifier
- `signature`: Cryptographic signature
- `public_key`: Verification public key
- `signature_type`: Type of signature used
- `metadata`: Additional metadata

**Raises:**
- `AuthenticationError`: Invalid API key
- `RateLimitError`: Rate limit exceeded
- `QuotaExceededError`: Monthly quota exceeded
- `QRNGError`: Other API errors

#### `health()`

Get system health status.

**Returns:** `HealthStatus` with NIST test results

### QRNGStreamClient

#### `connect(on_data, chunk_size=32, format="hex", on_error=None, on_close=None)`

Connect to WebSocket stream.

**Parameters:**
- `on_data` (Callable): Callback for each data chunk
- `chunk_size` (int): Size of each chunk in bytes
- `format` (str): Output format
- `on_error` (Callable, optional): Error callback
- `on_close` (Callable, optional): Close callback

## Error Handling

```python
from qrng import QRNGClient, AuthenticationError, RateLimitError, QuotaExceededError

client = QRNGClient(api_key="qnrk_...")

try:
    result = client.generate(bytes=32)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded - slow down")
except QuotaExceededError:
    print("Monthly quota exceeded - upgrade plan")
except Exception as e:
    print(f"Error: {e}")
```

## Requirements

- Python 3.8+
- `requests >= 2.25.0`
- `websocket-client >= 1.0.0`

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://qrngapi.com/docs
- Issues: https://github.com/qrng-api/python-sdk/issues
- Email: support@qrngapi.com
