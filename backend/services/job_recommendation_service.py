from backend.data.role_skills import ROLE_SKILLS


def suggest_job(skills):

    best_role = "Software Engineer"

    max_match = 0

    for role, required_skills in ROLE_SKILLS.items():

        score = len(
            set(skills)
            &
            set(required_skills)
        )

        if score > max_match:

            max_match = score
            best_role = role


    descriptions = {

        "Backend Developer":
        "Looking for a Backend Developer with experience in Python, FastAPI, SQL, APIs and Docker.",

        "Frontend Developer":
        "Looking for a Frontend Developer with experience in JavaScript, React, HTML and CSS.",

        "Full Stack Developer":
        "Looking for a Full Stack Developer with frontend and backend experience.",

        "Data Scientist":
        "Looking for a Data Scientist with experience in Python, Machine Learning, NLP, Data Analytics and Deep Learning.",

        "Data Analyst":
        "Looking for a Data Analyst with SQL, Excel, Power BI and visualization skills.",

        "ML Engineer":
        "Looking for an ML Engineer with experience in Python, TensorFlow, PyTorch and model deployment.",

        "DevOps Engineer":
        "Looking for a DevOps Engineer with Docker, Kubernetes and cloud experience.",

        "Cloud Engineer":
        "Looking for a Cloud Engineer with AWS, Azure and cloud infrastructure experience.",

        "Cyber Security Analyst":
        "Looking for a Cyber Security Analyst with networking and security knowledge.",

        "Product Manager":
        "Looking for a Product Manager with leadership and agile experience.",

        "UI UX Designer":
        "Looking for a UI/UX Designer with Figma and design skills.",

        "HR Specialist":
        "Looking for an HR Specialist with communication and recruitment skills.",

        "Digital Marketing Specialist":
        "Looking for a Digital Marketing Specialist with SEO and marketing expertise.",

        "Sales Executive":
        "Looking for a Sales Executive with negotiation and communication skills.",

        "Financial Analyst":
        "Looking for a Financial Analyst with accounting and analytical skills.",

        "Software Engineer":
        "Looking for a Software Engineer with strong programming and problem-solving skills."
    }

    return {

        "role": best_role,

        "job_description":
        descriptions.get(
            best_role,
            "Looking for a Software Engineer."
        )
    }