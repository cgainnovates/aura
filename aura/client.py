import requests
from . import config


class AuraError(Exception):
    pass


class ModelClient:
    def __init__(self):
        self.url = f"{config.BASE_URL}/chat/completions"
        self.headers = {"Authorization": f"Bearer {config.API_KEY}"}

    def chat(self, messages):
        payload = {
            "model": config.MODEL,
            "messages": messages
        }
        try:
            response = requests.post(
                self.url, json=payload, headers=self.headers, timeout=30
            )
        except requests.exceptions.Timeout:
            raise AuraError("Request Timeout. Try again")
        except requests.exceptions.ConnectionError:
            raise AuraError("Network problem. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise AuraError(f"Request failed: {e}")
        if response.status_code != 200:
            if response.status_code in (401, 403):
                raise AuraError(f"Error {response.status_code}: API key rejected. Check AURA_API_KEY in .env")
            elif response.status_code == 404:
                raise AuraError(f"Error {response.status_code}: Model not found. Check AURA_MODEL in .env")
            elif response.status_code == 429:
                raise AuraError(f"Error {response.status_code}: Rate limit reached. Wait a moment and try again." )
            elif response.status_code >= 500:
                raise AuraError(f"Error {response.status_code}: The provider is having problems. Try again later.")
            else:
                raise AuraError(f"Error {response.status_code}: An unknown error occurred")
        data = response.json()
        return data["choices"][0]["message"]["content"]