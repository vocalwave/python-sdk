"""QRNG API WebSocket streaming client."""

import json
import websocket
from typing import Callable, Optional, Literal
from threading import Thread

from .errors import QRNGError, AuthenticationError


FormatType = Literal["hex", "base64", "binary", "uint8", "uint32"]


class QRNGStreamClient:
    """
    QRNG API WebSocket streaming client.
    
    Example:
        >>> def on_data(data):
        ...     print(f"Received: {data}")
        >>> 
        >>> client = QRNGStreamClient(api_key="qnrk_...")
        >>> client.connect(on_data=on_data, chunk_size=32, format="hex")
        >>> # Data streams continuously...
        >>> client.disconnect()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "wss://qrngapi.com"
    ):
        """
        Initialize streaming client.
        
        Args:
            api_key: Your QRNG API key
            base_url: WebSocket base URL (default: wss://qrngapi.com)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.ws: Optional[websocket.WebSocketApp] = None
        self.thread: Optional[Thread] = None
    
    def connect(
        self,
        on_data: Callable[[str], None],
        chunk_size: int = 32,
        format: FormatType = "hex",
        on_error: Optional[Callable[[Exception], None]] = None,
        on_close: Optional[Callable[[], None]] = None
    ):
        """
        Connect and start streaming entropy.
        
        Args:
            on_data: Callback function for each data chunk
            chunk_size: Size of each chunk in bytes (1-1024)
            format: Output format
            on_error: Optional error callback
            on_close: Optional close callback
        """
        ws_url = f"{self.base_url}/api/stream?chunkSize={chunk_size}&format={format}"
        
        def on_ws_message(ws, message):
            try:
                data = json.loads(message)
                if "error" in data:
                    error = QRNGError(data["error"])
                    if on_error:
                        on_error(error)
                elif "data" in data:
                    on_data(data["data"])
            except Exception as e:
                if on_error:
                    on_error(e)
        
        def on_ws_error(ws, error):
            if on_error:
                on_error(QRNGError(str(error)))
        
        def on_ws_close(ws, close_status_code, close_msg):
            if on_close:
                on_close()
        
        def on_ws_open(ws):
            # Send authentication
            ws.send(json.dumps({"apiKey": self.api_key}))
        
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_ws_open,
            on_message=on_ws_message,
            on_error=on_ws_error,
            on_close=on_ws_close
        )
        
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
    
    def disconnect(self):
        """Disconnect from the stream."""
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join(timeout=5)
