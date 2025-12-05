from sqlalchemy import Column, Integer, Text
from .database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)  # id de usuario de IAM
