import os
import re
import requests

from dotenv import load_dotenv

# Load .env file explicitly from current directory
load_dotenv()

# Load API key from environment variable
NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")

# Numverify API endpoint
NUMVERIFY_URL = "http://apilayer.net/api/validate"


def extract_phone_number(text: str):
    # Extracts and cleans a phone number from user input.
    match = re.search(r"\+?[0-9][0-9\-\s\(\)]{6,20}", text)
    if not match:
        return None

    raw_number = match.group(0).strip()
    cleaned_number = re.sub(r"[^\d+]", "", raw_number)

    if cleaned_number.count("+") > 1:
        return None
    if "+" in cleaned_number and not cleaned_number.startswith("+"):
        return None

    return cleaned_number


def call_numverify_api(phone_number: str) -> dict:
    # Sends request to Numverify API and returns JSON response.
    if not NUMVERIFY_API_KEY:
        return {"error": {"info": "NUMVERIFY_API_KEY is not set."}}

    params = {
        "access_key": NUMVERIFY_API_KEY,
        "number": phone_number,
        "format": 1
    }

    try:
        response = requests.get(NUMVERIFY_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": {"info": f"Request failed: {e}"}}


def format_numverify_response(data: dict, phone_number: str) -> str:
    # Converts API JSON into natural language response.
    if "error" in data:
        error_message = data["error"].get("info", "Unknown error.")
        return f"I couldn't validate that number right now. Reason: {error_message}"

    if not data.get("valid", False):
        return f"I checked {phone_number}, and it does not appear to be a valid phone number."

    country = data.get("country_name") or "an unknown country"
    location = data.get("location") or "an unknown region"
    carrier = data.get("carrier") or "an unknown carrier"
    line_type = data.get("line_type") or "an unknown type"
    intl_format = data.get("international_format") or phone_number

    return (
        f"I checked that number for you. It appears valid. "
        f"It is associated with {country}, specifically {location}. "
        f"It looks like a {line_type} number, and the carrier is {carrier}. "
        f"The international format is {intl_format}."
    )


def phone_lookup_service(user_input: str) -> str:
    # Main service: extract number, call API, return formatted result.
    phone_number = extract_phone_number(user_input)

    if not phone_number:
        return "Please provide a phone number in international format (e.g., +14165551234)."

    data = call_numverify_api(phone_number)
    return format_numverify_response(data, phone_number)


# Simple test block to run this file directly
if __name__ == "__main__":
    user_input = input("Enter a phone number or message: ")
    result = phone_lookup_service(user_input)
    print("\nResponse:")
    print(result)