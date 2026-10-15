import time
import requests
from . import config


class AuraError(Exception):
    pass


class ModelClient:
    def __init__(self):
        self.url = f"{config.BASE_URL}/chat/completions"
        self.headers = {"Authorization": f"Bearer {config.API_KEY}"}


    def _request(self, messages):
        payload = {
            "model": config.MODEL,
            "messages": messages,
            "max_completion_tokens": 1024
        }
        max_attempt = 3
        for attempt in range(max_attempt):
            is_last = attempt == max_attempt - 1
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
                    if is_last:
                        raise AuraError(
                            f"Error {response.status_code}: Rate limit reached. Wait a moment and try again.")
                    wait = self._wait_time(response, attempt)
                    print(f"[rate limited, retrying in {wait}s...]")
                    time.sleep(wait)
                    continue
                elif response.status_code >= 500:
                    raise AuraError(f"Error {response.status_code}: The provider is having problems. Try again later.")
                else:
                    raise AuraError(f"Error {response.status_code}: An unknown error occurred")
            return response.json()


    def chat(self, messages):
        data = self._request(messages)
        return data["choices"][0]["message"]["content"]

    def _wait_time(self, response, attempt):
        try:
            return min(int(response.headers['retry-after']), 30)
        except (KeyError, ValueError):
            return 2**attempt