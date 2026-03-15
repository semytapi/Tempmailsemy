from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "TempMail API Running"


@app.route("/mail")
def mail():

    action = request.args.get("action")
    key = request.args.get("key")

    try:

        # NEW EMAIL
        if action == "new":

            r = requests.get(
                "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
                timeout=10
            )

            data = r.json()
            email = data[0]

            return jsonify({
                "status": "success",
                "email": email
            })


        # CHECK INBOX
        if key == "semy" and action:

            email = action
            login, domain = email.split("@")

            r = requests.get(
                f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}",
                timeout=10
            )

            return jsonify({
                "email": email,
                "messages": r.json()
            })

        return jsonify({"error": "invalid request"})


    except Exception as e:
        return jsonify({
            "error": str(e)
        })
