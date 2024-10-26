from sqlalchemy.orm.session import Session
from schemas import MessageBase
from db.models import DbMessage

def save_message(db: Session, body: MessageBase):
    new_message = DbMessage(
        sender_id=body.user_id, 
        recipient_id=body.recipient_id, 
        content=body.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message