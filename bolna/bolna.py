from bolna_call import BolnaCall
from bolna_fetch import BolnaFetch
import json
import time

def main():
    # Initialize BolnaCall with required parameters
    agent_id = "a83ecf8f-4d03-4a72-9d4e-98692c8e757f"
    recipient_phone_number = "+918590351989"
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

    # Wait until the status is 'completed' or 'busy'
    while status not in ["completed", "busy"]:
        print(f"Current status: {status}. Waiting...")
        time.sleep(30)  # Delay for 30 seconds before checking again
        call_response = bolna_call.make_call()  # Recheck the status
        try:
            call_response_data = json.loads(call_response)
            status = call_response_data.get("status")
        except json.JSONDecodeError as e:
            print(f"Failed to parse call response during status check: {e}")
            return

    # Initialize BolnaFetch with the extracted execution_id
    bolna_fetch = BolnaFetch(execution_id, auth_token)
    try:
        fetch_response = bolna_fetch.fetch_output()
        print("Fetch Response:", fetch_response)
    except Exception as e:
        print(f"Error fetching output: {e}")

if __name__ == "__main__":
    main()