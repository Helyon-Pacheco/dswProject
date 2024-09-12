from pydantic import BaseModel
from ..enums.notification_type import NotificationType

class Notification(BaseModel):
    message: str
    type: NotificationType

    class Config:
        use_enum_values = True
