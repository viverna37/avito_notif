from sqlalchemy import Column, Integer, TEXT
from .db import Base


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_id = Column(TEXT)
