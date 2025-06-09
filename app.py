from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from booking_handler import handle_booking

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