from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database.db import Base


class ResumeSkill(Base):

    __tablename__ = "resume_skills"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resume.id"))

    skill_name = Column(String, nullable=False)