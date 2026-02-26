import httpx
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8080/api/v1"
API_KEY = "b7a15e1f9f9305d95b22226d615a93d5"


def create_lead(lead_data):
    url = f"{BASE_URL}/CLeadAnalysis"

    headers = {

        "X-Api-Key": API_KEY
    }

    response = httpx.post(
        url,
        json=lead_data,
        headers=headers,
        timeout=10.0
    )

    response.raise_for_status()
    return response.json()


def send_mock_payload(file_path: str | None = None):
    """Load a mock JSON file, flatten and remap keys, print payload, and send to CRM.
    If file_path is None, defaults to mock_outputs/analysis_1.json next to the project root.
    Returns the response JSON from the CRM endpoint.
    """
    mock_file = None
    if file_path:
        mock_file = Path(file_path)
    else:
        mock_file = Path(__file__).resolve().parents[1] / "mock_outputs" / "analysis_1.json"

    with mock_file.open("r", encoding="utf-8") as f:
        lead_payload = json.load(f)

    # Flatten payload: move children of the nested "analysis" object to top-level
    analysis = lead_payload.get("analysis")
    if isinstance(analysis, dict):
        for k, v in analysis.items():
            lead_payload[k] = v
        lead_payload.pop("analysis", None)

    # Remap keys to match CRM labels (user-requested label names)
    key_map = {
        "intent_level": "intentlevel",
        "budget_fit": "budgetfit",
        "timeline_readiness": "timeline_readiness",
        "followup_ready": "followupready",
        "faq_engagement_level": "faqengagementlevel",
        "overall_interest_score": "overall_interest_score",
        "ai_score": "aiscore",
        "crm_category": "crmcategory",
    }

    for old_key, new_key in key_map.items():
        if old_key in lead_payload:
            val = lead_payload.pop(old_key)
            # convert boolean followup flag to lowercase string if needed
            if new_key == "followupready":
                if isinstance(val, bool):
                    val = str(val).lower()
            lead_payload[new_key] = val

    # Print the flattened and remapped payload to the terminal before sending
    print("Payload to send:")
    print(json.dumps(lead_payload, indent=2))

    result = create_lead(lead_payload)
    return result


def prepare_payload(lead_payload: dict) -> dict:
    """Flatten and remap a payload dict (no I/O).
    Returns the transformed payload ready to send to CRM.
    """
    payload = dict(lead_payload)  # shallow copy to avoid mutating caller

    # Flatten payload: move children of the nested "analysis" object to top-level
    analysis = payload.get("analysis")
    if isinstance(analysis, dict):
        for k, v in analysis.items():
            payload[k] = v
        payload.pop("analysis", None)

    # Remap keys to match CRM labels (user-requested label names)
    key_map = {
        "intent_level": "intentLevel",
        "budget_fit": "budgetFit",
        "timeline_readiness": "timelineReadiness",
        "followup_ready": "followupReady",
        "faq_engagement_level": "faqEngagementLevel",
        "overall_interest_score": "overallInterestScore",
        "ai_score": "aiScore",
        "crm_category": "crmCategory",
    }

    for old_key, new_key in key_map.items():
        if old_key in payload:
            val = payload.pop(old_key)
            if new_key == "followupready":
                if isinstance(val, bool):
                    val = str(val).lower()
            payload[new_key] = val

    return payload


def send_payload(lead_payload: dict):
    """Prepare and send a payload dict directly to CRM."""
    prepared = prepare_payload(lead_payload)
    print("Payload to send:")
    print(json.dumps(prepared, indent=2))
    return create_lead(prepared)


if __name__ == "__main__":
    try:
        arg = sys.argv[1] if len(sys.argv) > 1 else None
        result = send_mock_payload(arg)
        print("Lead created successfully.")
        print("Lead ID:", result.get("id"))
    except httpx.HTTPStatusError as e:
        print("HTTP error:", e.response.status_code, e.response.text)
    except Exception as e:
        print("Error:", str(e))