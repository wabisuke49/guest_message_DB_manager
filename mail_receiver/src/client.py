"""Send validated message data to the Phase 2 API."""

import requests


API_URL = "http://localhost:8000/messages"



def send_message_data(message_data: dict[str, str]) -> int:
    """POST message data as JSON and return the response status."""
    
    response = requests.post(API_URL, json=message_data)

    return response.status_code
