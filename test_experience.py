from backend.utils.experience_extractor import (
    extract_experience,
    categorize_experience
)

text = """
Python Developer with 4 years experience
in FastAPI and SQL.
"""

years = extract_experience(text)

category = categorize_experience(years)

print(years)

print(category)