from pydantic import BaseModel
from typing import Optional

class NotificationBase(BaseModel):
    title: str
    description: str

class NotificationCreate(NotificationBase):
    # si quieres que el user lo ponga explícitamente:
    user_id: Optional[int] = None

class NotificationOut(NotificationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
