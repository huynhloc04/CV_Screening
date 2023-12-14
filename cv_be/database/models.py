from sqlmodel import SQLModel, Field
from typing import Optional, List, Any
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from datetime import datetime
from enum import Enum

class TimeMixin(BaseModel):
    """Mixin class for datetime value of when the entity was created and when it was last modified. """

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    )
    
    
class Project(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    project_name: List[str]
    time: List[str]
    position: List[str]
    domain: List[str]    
    used_technologies: List[str]
    detailed_descriptions: List[str]
    
    
class Experience(SQLModel, table=True):
    id: int = Field(primary_key=True)
    commpany_name: List[str]
    time: List[str]
    position: List[str]
    domain: List[str]    
    used_technologies: List[str]
    detailed_descriptions: List[str]
    
    
class PersonalInformation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    earliest_university_year: str
    earliest_university_name: str
    birthday: str    
    gender: str
    nationality: str
    desired_position: str
    desired_salary: str
    desired_work_location: str
    
    
class Address(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    street: str
    ward: str
    district: str
    province: str
    
class ContactInformation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    phone: List[str]
    email: List[str]
    address_id: Optional[int] = Field(foreign_key="address.id")
    urls: List[str]
    
    
class Education(SQLModel, table=True):
    id: int = Field(primary_key=True)
    institution_name: List[str]
    time: List[str]
    degree: List[str]
    major: List[str]
    gpa: List[str]
    
    
class Skill(SQLModel, table=True):
    id: int = Field(primary_key=True)
    spoken_language: List[str]
    programming_language: List[str]
    soft_skill: List[str]
    hard_skill: List[str]
    
    
class Certificate(SQLModel, table=True):
    id: int = Field(primary_key=True)
    language_certificates: List[str]
    other_certificates: List[str]
    
    
class Reference(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: List[str]
    company: List[str]
    phone: List[str]
    email: List[str]
    
    
class Publication(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: List[str]
    author_name: List[str]
    year: List[str]
    
    
class IQ(SQLModel, table=True):
    id: int = Field(primary_key=True)
    iq_level: str
    explanation: str
    
    
class EQ(SQLModel, table=True):
    id: int = Field(primary_key=True)
    self_awareness_level: str
    self_regulation_level: str
    motivation_level: str
    empathy_level: str
    social_skills_level: str
    explanation: str
    

class CV(SQLModel, TimeMixin, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    cv_name: str
    project_id: Optional[int] = Field(foreign_key="project.id")
    exper_id: Optional[int] = Field(foreign_key="experience.id")
    strength: str
    weakness: str
    numerology: str
    personal_info_id: Optional[int] = Field(foreign_key="personalinformation.id")
    contact_info_id: Optional[int] = Field(foreign_key="contactinformation.id")
    education_id: Optional[int] = Field(foreign_key="education.id")
    skill_id: Optional[int] = Field(foreign_key="skill.id")
    cert_id: Optional[int] = Field(foreign_key="certificate.id")
    refer_id: Optional[int] = Field(foreign_key="reference.id")
    public_id: Optional[int] = Field(foreign_key="publication.id")
    achievements_and_honors: List[str]
    objective: List[str]
    social_activities: List[str]
    iq_id: Optional[int] = Field(foreign_key="iq.id")
    eq_id: Optional[int] = Field(foreign_key="eq.id")
    industry: List[str]
    summary: str