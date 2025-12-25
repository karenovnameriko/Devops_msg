import requests


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id

    def send_message(self, text: str):
        r = requests.post(
            f"{self.base_url}/sendMessage",
            json={"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=10
        )
        r.raise_for_status()

    def send_file(self, path: str):
        with open(path, "rb") as f:
            r = requests.post(
                f"{self.base_url}/sendDocument",
                data={"chat_id": self.chat_id},
                files={"document": f},
                timeout=20
            )
        r.raise_for_status()
