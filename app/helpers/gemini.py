import re
import os
import json
import google.generativeai as genai
from google.generativeai import GenerativeModel

genai.api_key = os.getenv("GEMINI_API_KEY")
model = GenerativeModel(
    model_name="gemini-2.5-flash")

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
    except (json.JSONDecodeError, AttributeError) as e:
        print("Error parsing JSON:", e)
        return []

def suggest_scientific_name(partial_name):
    prompt = f"""
    The user typed a partial scientific plant name: "{partial_name}".
    Suggest 5 possible complete scientific plant names that match.
    Return as a JSON array of strings, e.g.:
    ["Ficus lyrata", "Ficus benjamina", "Ficus elastica", "Ficus carica", "Ficus pumila"]
    """

    try:
        response = model.generate_content(prompt)
        print("Raw Gemini response:", response.text)
        # Extract JSON array from text to avoid parsing errors
        match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if not match:
            print("No JSON array found in response")
            return []
        json_str = match.group(0)
        return json.loads(json_str)

    except Exception as e:
        print(f"Error during Gemini generation: {e}")
        return []
