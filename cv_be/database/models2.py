from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from datetime import datetime

class TimeMixin(BaseModel):
    """Mixin class for datetime value of when the entity was created and when it was last modified. """

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    )

class CvBase(SQLModel):
    cv_status: str 
    cv_filename: str

class CV(CvBase, TimeMixin,table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    

