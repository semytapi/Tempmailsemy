import requests
import re
import random

def extract_otp(text):
    otp = re.findall(r'\b\d{4,8}\b', text)
    if otp:
        return otp[0]
    return None


def handler(request):

    action = request.args.get("action")
    key = request.args.get("key")

    # NEW EMAIL
    if action == "new":

        apis = [
            "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
            "https://api.tempmail.lol/generate"
        ]

        api = random.choice(apis)

        if "1secmail" in api:
            r = requests.get(api).json()
            email = r[0]

        else:
            r = requests.get(api).json()
            email = r["address"]

        return {
            "status": "success",
            "email": email
        }

    # CHECK INBOX
    if key == "semy" and action:

        email = action
        login, domain = email.split("@")

        r = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        ).json()

        messages = []

        for msg in r:
            msg_id = msg["id"]

            mail = requests.get(
                f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
            ).json()

            text = mail.get("body", "")
            otp = extract_otp(text)

            messages.append({
                "from": mail.get("from"),
                "subject": mail.get("subject"),
                "otp": otp,
                "text": text
            })

        return {
            "email": email,
            "messages": messages
        }

    return {
        "error": "invalid request"
    }
