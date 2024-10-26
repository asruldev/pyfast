from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from configs.config_app import APP_CONFIG, add_middlewares
from middlewares.middleware import log_requests, add_latency_to_response
from exceptions.exception import StoryException, story_exception_handler
from router import user, article, blog_get, blog_post, product, authentication, file, template, dependency, document, lokasi, report, shio, quran, chat
from datetime import datetime

from sqlalchemy.orm import Session
from db.database import engine
from db import models
from db.actions import db_user
from db.database import get_db

from client import html_1, html_2
import uvicorn
import logging
import json

logging.basicConfig(level=logging.INFO)

# Inisialisasi aplikasi
app = FastAPI(**APP_CONFIG)

# Tambahkan middleware
add_middlewares(app)
app.middleware("http")(log_requests)
app.middleware("http")(add_latency_to_response)

# Tangani exception khusus
app.add_exception_handler(StoryException, story_exception_handler)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, receiver_id: int):
        websocket = self.active_connections.get(receiver_id)
        if websocket:
            await websocket.send_text(json.dumps(message))
            print(f"Message sent to user {receiver_id}: {message}")
        else:
            print(f"No active connection for user {receiver_id}")

manager = ConnectionManager()

@app.get("/")
async def index():
    return HTMLResponse(html_1)

@app.get("/dua")
async def index():
    return HTMLResponse(html_2)

# Mount router
app.include_router(authentication.router)
app.include_router(quran.router)
app.include_router(shio.router)
app.include_router(report.router)
app.include_router(lokasi.router)
app.include_router(dependency.router)
app.include_router(document.router)
app.include_router(file.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(template.router)

# Mount WebSocket handler
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            message_data = json.loads(data)

            # Validasi format pesan
            if "receiver_id" not in message_data or "content" not in message_data:
                print("Invalid message format")
                continue

            # Menyimpan pesan di database
            new_message = db_user.save_message(db, user_id, message_data)

            # Kirim pesan kepada penerima
            await manager.send_personal_message(
                {
                    "sender_id": new_message.sender_id,
                    "recipient_id": new_message.recipient_id,
                    "content": new_message.content,
                    "is_read": new_message.is_read,
                    "send_at": new_message.send_at.isoformat(),
                    "read_at": new_message.read_at.isoformat() if new_message.read_at else None,
                    "is_deleted": new_message.is_deleted,
                    "deleted_at": new_message.deleted_at.isoformat() if new_message.deleted_at else None,
                },
                message_data["receiver_id"],
            )
            # await manager.send_personal_message(
            #     {
            #         "sender_id": new_message.sender_id,
            #         "recipient_id": new_message.recipient_id,
            #         "content": new_message.content,
            #         "is_read": new_message.is_read,
            #         "send_at": new_message.send_at.isoformat(),
            #         "read_at": new_message.read_at.isoformat() if new_message.read_at else None,
            #         "is_deleted": new_message.is_deleted,
            #         "deleted_at": new_message.deleted_at.isoformat() if new_message.deleted_at else None,
            #     },
            #     user_id,
            # )
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(user_id)

# Mount folder statis
app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount('/templates/static', StaticFiles(directory='templates/static'), name='static')

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)
