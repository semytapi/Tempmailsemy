from flask import Flask, request, jsonify
import requests
import json

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

            data = json.loads(r.text)

            return jsonify({
                "email": data[0]
            })


        # CHECK INBOX
        if key == "semy" and action:

            login, domain = action.split("@")

            r = requests.get(
                f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}",
                timeout=10
            )

            data = json.loads(r.text)

            return jsonify({
                "email": action,
                "messages": data
            })


        return jsonify({"error": "invalid request"})


    except Exception as e:
        return jsonify({"error": str(e)})
