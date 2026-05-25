from dotenv import load_dotenv
import os
import requests

load_dotenv()

BOT_TOKEN = os.getenv("8936512534:AAGxFC9AIxbJDXPUBYZ2gsUq07MEy7wM3ZU")
CHAT_ID = os.getenv("7366145742")


class TelegramAlerts:

    @staticmethod
    def send_message(message):

        if not BOT_TOKEN or not CHAT_ID:
            print("Telegram environment variables missing")
            return

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        try:

            response = requests.post(
                url,
                data=payload,
                timeout=10
            )

            if response.status_code == 200:
                print("Telegram Alert Sent")
            else:
                print(f"Telegram Failed: {response.text}")

        except Exception as e:

            print(f"Telegram Error: {e}")