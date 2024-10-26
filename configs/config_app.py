from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
import logging

# Pengaturan logging
logging.basicConfig(level=logging.INFO)

description = """
## WebSocket Chat

Untuk mengakses WebSocket di `/ws/chat/userId`, Anda dapat menggunakan JavaScript berikut ini di konsol browser:

```javascript
const socket = new WebSocket("ws://localhost:8888/ws/chat/userId");
socket.onmessage = function(event) { 
    console.log(event.data);
};
socket.onopen = function(event) {
    socket.send("Hello WebSocket!"); 
};
```
"""

# Konfigurasi aplikasi
APP_CONFIG = {
    "title": "My API",
    "description": description,
    "version": "1.0.0",
    "docs_url": "/swagger",
    "redoc_url": None,
    "openapi_url": "/openapi.json"
}

# Origins CORS
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://yourdomain.com"
]

def add_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)