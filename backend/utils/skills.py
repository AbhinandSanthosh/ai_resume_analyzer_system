import re

SKILLS_DB = [

    # Programming Languages
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "sql",

    # Web Development
    "html",
    "css",
    "react",
    "angular",
    "nodejs",
    "fastapi",
    "django",
    "flask",

    # Data Science / AI
    "machine learning",
    "deep learning",
    "data science",
    "nlp",
    "computer vision",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",

    # Cloud / DevOps
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "jenkins",
    "terraform",
    "ansible",
    "devops",
    "ci/cd",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",

    # Tools
    "git",
    "github",
    "streamlit",
    "power bi",
    "excel",
    "jupyter notebook",

    # AI Tools
    "huggingface",
    "langchain",
    "openai",

    # Mobile Development
    "android",
    "ios",
    "flutter",
    "react native",
    "swift",
    "kotlin",

    # Data Analytics
    "tableau",
    "statistics",
    "data visualization",
    "eda",
    "predictive modeling",

    # Cyber Security
    "ethical hacking",
    "network security",
    "penetration testing",
    "linux",
    "cryptography",

    # UI/UX
    "figma",
    "adobe xd",
    "wireframing",
    "prototyping",

    # Product / Management
    "agile",
    "scrum",
    "jira",
    "project management",

    # HR
    "recruitment",
    "talent acquisition",

    # Marketing
    "seo",
    "content marketing",
    "google analytics",
    "social media marketing",

    # Finance / Business
    "financial modeling",
    "accounting",
    "business analysis",

    # Sales
    "negotiation",
    "customer relationship management",

    # Soft Skills
    "leadership",
    "communication",
    "teamwork",
    "problem solving",
    "critical thinking",
    "time management"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills