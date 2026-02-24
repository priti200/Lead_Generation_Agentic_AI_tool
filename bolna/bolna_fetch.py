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

if __name__ == "__main__":
    execution_id = "af1e7820-3342-41fe-bd7b-e44049ca1c9f"
    auth_token = "bn-3cab50fdf99b4f85909e7fcd465f76b5"
    
    bolna_fetcher = BolnaFetch(execution_id, auth_token)
    output = bolna_fetcher.fetch_output()
    print(output)