import os
import requests

def query_google_gemini_for_plant(common_name: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY is not set")

    # This is a hypothetical endpoint and request — replace with actual Gemini API details
    url = "https://gemini.googleapis.com/v1/your_model_endpoint"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Provide detailed botanical info for the plant named '{common_name}', including scientific name, preferred soil conditions, propagation methods, edible parts, and whether it's safe for household pets."

    body = {
        "prompt": prompt,
        "max_tokens": 300
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Parse response - depends on how Gemini API returns data
    # Let's assume it returns a JSON object with these fields:
    return {
        "scientific_name": data.get("scientific_name"),
        "preferred_soil_conditions": data.get("preferred_soil_conditions"),
        "propagation_methods": data.get("propagation_methods"),
        "edible_parts": data.get("edible_parts"),
        "is_pet_safe": data.get("is_pet_safe"),
    }
