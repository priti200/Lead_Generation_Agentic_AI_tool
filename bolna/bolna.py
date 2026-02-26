from bolna_call import BolnaCall
from bolna_fetch import BolnaFetch
import json
import time
import subprocess
import os

def main():
    # Initialize BolnaCall with required parameters
    agent_id = "a83ecf8f-4d03-4a72-9d4e-98692c8e757f"
    recipient_phone_number = "+919072242443"
    auth_token = "bn-3cab50fdf99b4f85909e7fcd465f76b5"

    bolna_call = BolnaCall(agent_id, recipient_phone_number, auth_token)
    call_response = bolna_call.make_call()
    print("Call Response:", call_response)

    # Extract execution_id and status from the call response
    try:
        call_response_data = json.loads(call_response)
        execution_id = call_response_data.get("execution_id")
        status = call_response_data.get("status")
        if not execution_id:
            raise ValueError("Execution ID not found in the call response.")
    except json.JSONDecodeError as e:
        print(f"Failed to parse call response: {e}")
        return
    except ValueError as e:
        print(e)
        return

    bolna_fetch = BolnaFetch(execution_id, auth_token)

    # Wait until the status is 'completed' or 'busy'
    while status not in ["completed", "busy"]:
        print(f"Current status: {status}. Waiting...")
        time.sleep(2)  # Delay for 30 seconds before checking again
        call_response = bolna_fetch.fetch_output()  # Recheck the status
        try:
            call_response_data = json.loads(call_response)
            status = call_response_data.get("status")
        except json.JSONDecodeError as e:
            print(f"Failed to parse call response during status check: {e}")
            return

    # Initialize BolnaFetch with the extracted execution_id
    try:
        fetch_response = bolna_fetch.fetch_output()
        print("Fetch Response:", fetch_response)
        # Persist the raw Bolna response so the converter can read it
        os.makedirs("mock_inputs", exist_ok=True)
        try:
            parsed = json.loads(fetch_response)
        except Exception:
            parsed = fetch_response
        with open("mock_inputs/bolna_response.json", "w", encoding="utf-8") as fh:
            json.dump(parsed, fh, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error fetching output: {e}")

    # Assuming bolna_response.json is created earlier in the script
    response_file = "mock_inputs/bolna_response.json"
    if os.path.exists(response_file):
        print("bolna_response.json created. Running convert_summary_transcript.py...")
        subprocess.run(["python", "bolna/convert_summary_transcript.py"], check=True)
        print("convert_summary_transcript.py executed successfully.")

if __name__ == "__main__":
    main()