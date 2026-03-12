from flask import Flask, request, send_file
import random
import requests
import os

app = Flask(__name__)

# Replace with your real Telegram bot token and chat ID
BOT_TOKEN = "8770758706:AAFTkskfOpOHaZKN6vP__nwDzYvBwxqKH6E"
CHAT_ID = "5669491975"

otp = ""

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        response = requests.post(url, data=data, timeout=10)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram error:", e)

@app.route("/", methods=["GET", "POST"])
def home():
    global otp

    if request.method == "POST":
        user_otp = request.form.get("otp", "").strip()

        if user_otp == otp:
            return send_file("myfile.pdf", as_attachment=False)
        else:
            return """
            <h2>Wrong OTP</h2>
            <a href="/">Try Again</a>
            """

    otp = str(random.randint(1000, 9999))
    print("Generated OTP:", otp)
    send_telegram(f"OTP for PDF access: {otp}")

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF OTP Access</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                text-align: center;
                width: 320px;
            }
            input {
                width: 90%;
                padding: 10px;
                margin: 12px 0;
                font-size: 16px;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 18px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Enter OTP to Open PDF</h2>
            <form method="post">
                <input type="text" name="otp" placeholder="Enter OTP" required>
                <br>
                <button type="submit">Open PDF</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
