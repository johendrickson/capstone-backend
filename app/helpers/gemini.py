import os
import json
import google.generativeai as genai
from google.generativeai import GenerativeModel

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

# Set API key globally on the genai client
genai.set_api_key(api_key)

# Create model instance (no api_key param here)
model = GenerativeModel(model_name="gemini-2.5-flash")

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

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print("Error parsing Gemini JSON:", e)
        return {}

def suggest_scientific_name(partial_name):
    prompt = f"""
    The user typed a partial scientific plant name: "{partial_name}".
    Suggest 5 possible complete scientific plant names that match.
    Return as a JSON array of strings, e.g.:
    ["Ficus lyrata", "Ficus benjamina", "Ficus elastica", "Ficus carica", "Ficus pumila"]
    """

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print("Error parsing suggestions JSON:", e)
        return []
