import requests
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "HUGGINGFACE_API_KEY"
)

API_URL = (
    "https://api-inference.huggingface.co/models/"
    "google/flan-t5-base"
)

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def generate_ai_recommendation(
    missing_skills,
    matched_skills
):

    prompt = f"""
    A candidate has these skills:
    {matched_skills}

    Missing skills are:
    {missing_skills}

    Give professional resume improvement recommendations.
    """

    payload = {
        "inputs": prompt
    }

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        result = response.json()

        if isinstance(result, list):

            return result[0].get(
                "generated_text",
                "No recommendation generated"
            )

        return str(result)
    
    except Exception as e:
        
        print("FULL ERROR:", e)
        
        return f"ERROR: {str(e)}"