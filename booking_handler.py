import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import base64
import json

user_sessions = {}

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

def handle_booking(user_id, msg):
    session = user_sessions.get(user_id, {})

    if "step" not in session:
        session["step"] = "name"
        user_sessions[user_id] = session
        return "Welcome to Royal Spice! 🍽️ What's your name?"

    elif session["step"] == "name":
        session["name"] = msg
        session["step"] = "date"
        return "What date would you like to book for? (e.g., 9 June)"

    elif session["step"] == "date":
        session["date"] = msg
        session["step"] = "time"
        return "What time? (e.g., 8 PM)"

    elif session["step"] == "time":
        session["time"] = msg
        session["step"] = "guests"
        return "How many people?"

    elif session["step"] == "guests":
        session["guests"] = msg
        user_sessions.pop(user_id)

        # Store in Google Sheet
        try:
            sheet.append_row([
                session["name"],
                user_id,
                session["date"],
                session["time"],
                session["guests"]
            ])
            return f"✅ Table booked for {session['guests']} people on {session['date']} at {session['time']}. See you soon, {session['name']}!"
        except Exception as e:
            return "Sorry, there was an error saving your booking. Please try again later."

    return "Sorry, I didn't understand that. Please start again by saying 'book'."