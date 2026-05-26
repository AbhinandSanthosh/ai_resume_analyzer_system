import re


def extract_experience(resume_text):

    pattern = r"(\d+)\+?\s*(years|year)"

    matches = re.findall(
        pattern,
        resume_text.lower()
    )

    years = []

    for match in matches:

        years.append(
            int(match[0])
        )

    if years:

        return max(years)

    return 0


def categorize_experience(years):

    if years <= 1:

        return "Fresher"

    elif years <= 3:

        return "Junior"

    elif years <= 5:

        return "Mid-Level"

    else:

        return "Senior"