from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def extract_otp(text):
    otp = re.findall(r'\b\d{4,8}\b', text)
    return otp[0] if otp else None


@app.route("/mail")
def mail():

    action = request.args.get("action")
    key = request.args.get("key")

    # NEW EMAIL
    if action == "new":

        r = requests.get(
            "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        )

        email = r.json()[0]

        return jsonify({
            "status": "success",
            "email": email
        })


    # CHECK INBOX
    if key == "semy" and action:

        email = action
        login, domain = email.split("@")

        r = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        )

        messages = []

        for msg in r.json():

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

        return jsonify({
            "email": email,
            "messages": messages
        })

    return jsonify({
        "error": "invalid request"
    })
