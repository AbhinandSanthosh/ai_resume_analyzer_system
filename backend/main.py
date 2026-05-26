from fastapi import FastAPI

from backend.database.db import engine, Base

from backend.routes.user_routes import router as user_router
from backend.routes.resume_routes import router as resume_router

from backend.models.user_model import User
from backend.models.resume_model import Resume
from backend.models.skills_models import ResumeSkill
from backend.models.analysis_model import AnalysisResult

from backend.auth.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Resume AI System Running"
    }


app.include_router(user_router)
app.include_router(resume_router)
app.include_router(auth_router)