
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text, DateTime, Boolean
from db.database import Base
from sqlalchemy import Column
from datetime import datetime

class DbMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    send_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("DbUser", foreign_keys=[sender_id])
    recipient = relationship("DbUser", foreign_keys=[recipient_id])

    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()

    def delete_message(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
