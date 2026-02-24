import requests

class BolnaFetch:
    def __init__(self, execution_id, auth_token):
        self.url = f"https://api.bolna.ai/executions/{execution_id}"
        self.headers = {"Authorization": f"Bearer {auth_token}"}

    def fetch_output(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

            