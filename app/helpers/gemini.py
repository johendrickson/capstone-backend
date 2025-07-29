import os
import json
from google import generativeai

# Set API key via environment variable or directly in code (not recommended for security)
generativeai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_plant_info_from_scientific_name(scientific_name):
    prompt = f"""
    Provide detailed information about the plant with the scientific name "{scientific_name}".
    Return the following fields in JSON format:
    {{
        "common_name": "string",
        "species": "string",
        "preferred_soil_conditions": "string",
        "propagation_methods": "string",
        "edible_parts": "string",
        "is_pet_safe": true
    }}
    Only return the JSON object — no extra explanation or formatting.
    """

    response = generativeai.generate_text(
        model="gemini-1.5-pro",
        prompt=prompt,
        response_mime_type="application/json"
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {}

def suggest_scientific_name(partial_name):
    prompt = f"""
    The user typed a partial scientific plant name: "{partial_name}"
    Suggest 5 possible complete scientific plant names that match.
    Return as a JSON array of strings, e.g.:
    ["Ficus lyrata", "Ficus benjamina", "Ficus elastica", "Ficus carica", "Ficus pumila"]
    """

    response = generativeai.generate_text(
        model="gemini-1.5-pro",
        prompt=prompt,
        response_mime_type="application/json"
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return []
