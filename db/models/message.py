from sqlalchemy import Column, VARCHAR, BOOLEAN, Integer, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):
    __tablename__ = "messages"

    sender_id = Column(Integer(), ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    recipient_id = Column(Integer(), ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    message = Column(VARCHAR(280))  # Как в Твитторе
    is_delete = Column(BOOLEAN(), nullable=False, default=False)


