from sqlalchemy import Column, Integer, String, ForeignKey, Text
from backend.database.db import Base

class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    file_name = Column(String)

    extracted_text = Column(Text)

    experience_years = Column(Integer)

    experience_level = Column(String)

    suggested_role = Column(String)

    suggested_job_description = Column(Text)

