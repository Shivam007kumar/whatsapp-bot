from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from booking_handler import handle_booking
import os
import base64
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Decode base64 GOOGLE_CREDS env variable
creds_json = base64.b64decode(os.environ["GOOGLE_CREDS"]).decode("utf-8")
creds_dict = json.loads(creds_json)

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Restaurant Bookings").sheet1

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")

    response = MessagingResponse()
    reply = handle_booking(from_number, incoming_msg)
    response.message(reply)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)