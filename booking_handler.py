import gspread
from oauth2client.service_account import ServiceAccountCredentials

user_sessions = {}

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
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
        sheet.append_row([
            session["name"],
            user_id,
            session["date"],
            session["time"],
            session["guests"]
        ])

        return f"✅ Table booked for {session['guests']} people on {session['date']} at {session['time']}. See you soon, {session['name']}!"