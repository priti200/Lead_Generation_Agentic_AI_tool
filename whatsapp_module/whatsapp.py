import os
import requests
from typing import Any

API_KEY = "a36e242781cbda47e22d174c7942310c17daabaa418b5888ecf6430690cb0be7"
DEFAULT_URL = os.getenv("WASENDER_URL", "https://www.wasenderapi.com/api/send-message")


def _build_headers() -> dict:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def send_message(to: str, text: str, url: str | None = None, timeout: int = 10) -> Any:
    """Send a WhatsApp message via Wasender API.

    Args:
        to: recipient phone number in international format (e.g. +919876543210)
        text: message body
        url: optional override for the API endpoint
        timeout: request timeout in seconds

    Returns:
        Parsed JSON response from the API.
    """
    if API_KEY is None:
        raise RuntimeError("WASENDER_API_KEY is not set in environment")

    endpoint = url or DEFAULT_URL
    headers = _build_headers()
    payload = {"to": to, "text": text}

    resp = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Example message based on user's requested text
    message = """I understand you're exploring doctoral studies. May I briefly share how our Ph.D. program at Amrita Vishwa Vidyapeetham is structured? 
        Our doctoral programs are designed to develop high-impact researchers with strong methodological foundations and deep domain expertise. "
        If you're aiming for a research-driven career—whether in academia, industry, or policy—this program is structured to provide both intellectual depth and professional growth."""

    # Replace with recipient you want to test with or pass as env/arg
    recipient = os.getenv("TEST_WHATSAPP_RECIPIENT", "+919072242443")

    try:
        result = send_message(recipient, message)
        print("Message sent successfully:", result)
    except Exception as e:
        print("Failed to send message:", str(e))