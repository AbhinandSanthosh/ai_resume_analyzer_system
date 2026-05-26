from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

import shutil
import os

from backend.database.db import get_db
from backend.models.resume_model import Resume

from backend.utils.resume_parser import extract_text_from_resume
from backend.utils.skills import extract_skills

from backend.services.scoring_service import calculate_match_score

from backend.models.skills_models import ResumeSkill

from backend.schemas.job_schema import JobDescriptionRequest

from backend.services.scoring_service import calculate_match_score

from backend.models.analysis_model import AnalysisResult

from backend.utils.ml_matcher import (
    calculate_similarity
)

from backend.utils.experience_extractor import (
    extract_experience,
    categorize_experience
)

from backend.services.recommendation_service import generate_recommendations

from backend.services.job_recommendation_service import suggest_job

from backend.auth.auth_bearer import verify_token

from backend.auth.role_checker import RoleChecker

#from backend.services.recommendation_service import generate_recommendations

#from backend.services.ai_recommendation_service import (
 #generate_ai_recommendation
#)

allow_admin = RoleChecker(
    ["admin"]
)

allow_recruiter = RoleChecker(
    ["admin", "recruiter"]
)

allow_candidate = RoleChecker(
    ["admin", "recruiter", "candidate"]
)

router = APIRouter()


@router.post("/upload-resume")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):

    allowed_extensions = [".pdf", ".docx"]

    file_extension = "." + file.filename.split(".")[-1].lower()
    
    MAX_FILE_SIZE = 5 * 1024 * 1024
    
    file.file.seek(0, 2)
 
    file_size = file.file.tell()

    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException (
            status_code=400,
            detail="File size exceeds 5MB limit"
        )

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="ONLY PDF AND DOCX ARE ALLOWED"
        )


    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_resume(file_path)

    print("Extracted text:")
    print(extracted_text)
    print("Length:", len(extracted_text) if extracted_text else 0)

    if not extracted_text or not extracted_text.strip():
        
        raise HTTPException(
            status_code=400,
            detail="No readable text found in resume"
        )
    
    experience_years = extract_experience(
        extracted_text
        )
    
    experience_level = categorize_experience(
        experience_years
        )

    skills = extract_skills(extracted_text)

    job_suggestion = suggest_job(skills)

    required_skills = [ 
        "python",
        "sql",
        "fastapi",
        "docker"
    ]

    match_result = calculate_match_score(
        skills, 
        required_skills
    )

    print(match_result)

    new_resume = Resume(
        user_id=user_id,
        file_name=file.filename,
        extracted_text=extracted_text,
        experience_years=experience_years,
        experience_level=experience_level,
        suggested_role=job_suggestion["role"],
        suggested_job_description=
        job_suggestion["job_description"]
    )

    db.add(new_resume)

    db.commit()

    db.refresh(new_resume)

    for skill in skills:

        new_skill = ResumeSkill(
            resume_id=new_resume.id,
            skill_name= skill
        )

        db.add(new_skill)

        db.commit()

    return {
        "message": "Resume uploaded and stored successfully",
        "resume_id": new_resume.id,
        "skills": skills,
        "suggested_role": job_suggestion["role"],
        "suggested_job_description":job_suggestion["job_description"],
        "match_analysis" : match_result
    }

@router.get("/search-by-skill")
def search_by_skill(skill: str, db: Session = Depends(get_db)):

    results = db.query(ResumeSkill).filter(
        ResumeSkill.skill_name.ilike(f"%{skill}%")
    ).all()

    response = []

    for result in results:

        response.append({
            "resume_id": result.resume_id,
            "skill": result.skill_name
        })

    return response

@router.post("/match-job")
def match_job_description(
    request: JobDescriptionRequest,
    db: Session = Depends(get_db)
):

    required_skills = extract_skills(
        request.job_description
    )

    if not required_skills:

        raise HTTPException(
            status_code=400,
            detail="No recoganizable skills found in job description"
        )



    resumes = db.query(Resume).all()

    results = []

    for resume in resumes:

        resume_skills = db.query(ResumeSkill).filter(
            ResumeSkill.resume_id == resume.id
        ).all()

        extracted_resume_skills = [
            skill.skill_name for skill in resume_skills
        ]

        match_result = calculate_match_score(
            extracted_resume_skills,
            required_skills
        )

        ml_score = calculate_similarity(
            resume.extracted_text,
            request.job_description
            )
        
        final_score = round(
            (
                match_result["score"] * 0.6
                )
                +
                (
                    ml_score * 0.4
                ),
                2
            )
        
        recommendations = generate_recommendations(
            match_result["matched_skills"],
            match_result["missing_skills"],
            resume.experience_years
            )

        analysis = AnalysisResult(
            resume_id=resume.id,
            role="custom job description",
            score=int(final_score),
            missing_skills=",".join(
                match_result["missing_skills"]
            ),
            strengths=",".join(
                match_result["matched_skills"]
            ),
            recommendations=",".join(
                recommendations
            )
        )
        db.add(analysis)

        db.commit()

        results.append({
            "resume_id": resume.id,
            "file_name": resume.file_name,
            "match_score": final_score,
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
            "recommendations": recommendations
        })

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "required_skills": required_skills,
        "candidate_matches": results
    }

@router.get("/analysis-history")
def get_analysis_history(
    db: Session = Depends(get_db),
    user=Depends(allow_recruiter)
):

    history = db.query(AnalysisResult).all()

    response = []

    for analysis in history:

        response.append({
            "id": analysis.id,
            "resume_id": analysis.resume_id,
            "role": analysis.role,
            "score": analysis.score,
            "missing_skills": analysis.missing_skills,
            "strengths": analysis.strengths,
            "recommendations": analysis.recommendations,
            "created_at": analysis.created_at
        })

    return response

@router.get("/resume/{resume_id}")
def get_resume_details(
    resume_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=400,
            detail="Resume not found"
        )

    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "extracted_text": resume.extracted_text
    }

@router.delete("/resume/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=400,
            detail="Resume not found"
        )

    db.query(ResumeSkill).filter(
        ResumeSkill.resume_id == resume_id
    ).delete()

    db.query(AnalysisResult).filter(
        AnalysisResult.resume_id == resume_id
    ).delete()

    db.delete(resume)

    db.commit()

    return {
        "message": "Resume deleted successfully"
    }

@router.get("/candidate-rankings")
def candidate_rankings(
    db: Session = Depends(get_db),
    user=Depends(allow_recruiter)
):

    analyses = db.query(
        AnalysisResult
    ).all()

    rankings = []

    for analysis in analyses:

        resume = db.query(Resume).filter(
            Resume.id == analysis.resume_id
        ).first()

        if not resume:
            continue

        rankings.append({

            "resume_id": resume.id,

            "file_name": resume.file_name,

            "score": analysis.score,

            "experience_years":
            resume.experience_years,

            "experience_level":
            resume.experience_level

        })

    rankings.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return rankings

@router.get("/test-auth")
def test_auth(
    user=Depends(verify_token)
):

    return {
        "message":"JWT working",
        "user": user
    }