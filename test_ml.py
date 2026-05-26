from backend.utils.ml_matcher import (
    calculate_similarity
)

resume = """
Python FastAPI SQL Machine Learning
"""

job = """
Looking for Python backend developer
with FastAPI and SQL skills
"""

score = calculate_similarity(
    resume,
    job
)

print(score)