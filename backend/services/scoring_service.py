def calculate_match_score(
    resume_skills,
    required_skills
):

    matched_skills = list(
        set(resume_skills)
        &
        set(required_skills)
    )

    missing_skills = list(
        set(required_skills)
        -
        set(resume_skills)
    )

    if len(required_skills) == 0:

        score = 0

    else:

        score = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100


    return {

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "score": round(score,2)
    }