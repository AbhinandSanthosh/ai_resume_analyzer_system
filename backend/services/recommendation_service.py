def generate_recommendations(
    matched_skills,
    missing_skills,
    experience_years
):

    recommendations = []

    if len(matched_skills) >= 5:

        recommendations.append(
            "Strong technical skill coverage for this role"
        )

    if experience_years < 1:

        recommendations.append(
            "Add internships or practical projects"
        )

    for skill in missing_skills:

        recommendations.append(
            f"Consider improving {skill}"
        )

    return recommendations