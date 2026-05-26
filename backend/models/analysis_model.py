from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from backend.database.db import Base


class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resume.id"))

    role = Column(String, nullable=False)

    score = Column(Integer)

    missing_skills = Column(String)

    strengths = Column(String)

    recommendations = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)