from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional

class EntityBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="Id")
    created_at: datetime = Field(default_factory=datetime.now, alias="CreatedAt")
    created_by_user: Optional[str] = Field(None, alias="CreatedByUser")
    updated_at: Optional[datetime] = Field(None, alias="UpdatedAt")
    updated_by_user: Optional[str] = Field(None, alias="UpdatedByUser")
    is_deleted: bool = Field(default=False, alias="IsDeleted")

    def update(self):
        self.updated_at = datetime.now()

    def toggle_is_deleted(self):
        self.update()
        self.is_deleted = not self.is_deleted
