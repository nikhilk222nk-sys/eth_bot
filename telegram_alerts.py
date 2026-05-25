import requests


BOT_TOKEN = "8936512534:AAGxFC9AIxbJDXPUBYZ2gsUq07MEy7wM3ZU"
CHAT_ID = "7366145742"


class TelegramAlerts:

    @staticmethod
    def send_message(message):

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }

        try:

            requests.post(
                url,
                data=payload
            )

            print("Telegram Alert Sent")

        except Exception as e:

            print(f"Telegram Error: {e}")