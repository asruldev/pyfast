from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import Dict
from db.database import get_db
from db.actions import db_chat
from schemas import UserBase
from auth.oauth2 import get_current_user

# Placeholder untuk menyimpan WebSocket pengguna yang sedang terhubung
connected_users: Dict[int, WebSocket] = {}

async def chat_endpoint(
    websocket: WebSocket, 
    db: Session = Depends(get_db), 
    current_user: UserBase = Depends(get_current_user)
):
    await websocket.accept()
    user_id = current_user.id
    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            recipient_id, content = parse_message_data(data)

            # Simpan pesan ke database
            db_chat.save_message(db, {
                'user_id': user_id,
                'recipient_id': recipient_id,
                'content': content
            })

            # Kirim pesan ke penerima jika mereka sedang terhubung
            if recipient_id in connected_users:
                await connected_users[recipient_id].send_text(f"From {user_id}: {content}")
            else:
                # Jika penerima tidak terhubung, kirim pesan ke pengirim
                await websocket.send_text(f"User {recipient_id} is not connected.")
    except WebSocketDisconnect:
        # Hapus pengguna dari daftar yang terhubung saat koneksi terputus
        del connected_users[user_id]
    except Exception as e:
        # Menangani kesalahan lainnya
        await websocket.send_text(f"An error occurred: {str(e)}")

def parse_message_data(data: str) -> tuple[int, str]:
    """Parser untuk mendapatkan recipient_id dan isi pesan dari data."""
    try:
        recipient_id, content = data.split(":", 1)
        return int(recipient_id), content.strip()  # Menghapus spasi di sekitar konten
    except ValueError:
        raise ValueError("Invalid message format. Use 'recipient_id:message_content'")

clients = []

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)