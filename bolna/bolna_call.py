import requests

class BolnaCall:
    def __init__(self, agent_id, recipient_phone_number, auth_token):
        self.url = "https://api.bolna.ai/call"
        self.payload = {
            "agent_id": agent_id,
            "recipient_phone_number": recipient_phone_number,
        }
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def make_call(self):
        response = requests.post(self.url, json=self.payload, headers=self.headers)
        return response.text