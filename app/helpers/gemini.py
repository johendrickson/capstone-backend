import os
import json
from google.generativeai import GenerativeModel
from google.generativeai.types import Content
import google.generativeai as genai

# Configure API key correctly
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the model
model = GenerativeModel("gemini-1.5-flash")

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
        print("Gemini response:", response.text)
        return json.loads(response.text)
    except (json.JSONDecodeError, AttributeError, Exception) as e:
        print("Error parsing JSON:", e)
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
        print("Gemini suggestions response:", response.text)
        return json.loads(response.text)
    except (json.JSONDecodeError, AttributeError, Exception) as e:
        print("Error parsing suggestions JSON:", e)
        return []
