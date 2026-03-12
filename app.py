from flask import Flask, request, send_file
import random
import requests

app = Flask(__name__)

# Telegram Bot details
BOT_TOKEN = "8770758706:AAFTkskfOpOHaZKN6vP__nwDzYvBwxqKH6E"
CHAT_ID = "5669491975"

otp = ""

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        r = requests.post(url, data=data)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Telegram error:", e)

@app.route("/", methods=["GET","POST"])
def home():
    global otp

    if request.method == "POST":
        user_otp = request.form.get("otp")

        if user_otp == otp:
            print("Correct OTP. Opening PDF.")
            return send_file("myfile.pdf")
        else:
            return "Wrong OTP"

    otp = str(random.randint(1000,9999))
    print("Generated OTP:", otp)

    send_telegram(f"OTP for PDF access: {otp}")

    return '''
    <h2>Enter OTP to open PDF</h2>
    <form method="post">
        <input name="otp" placeholder="Enter OTP">
        <button type="submit">Open PDF</button>
    </form>
    '''

app.run(debug=True)