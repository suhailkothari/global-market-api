from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# YOUR STOCK LIST
# -----------------------------
stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "7203.T",
    "6758.T",
    "AAPL",
    "MSFT"
]

latest_data = []

# -----------------------------
# FETCH DATA FUNCTION
# -----------------------------
def fetch_stock_data():
    global latest_data

    data_list = []

    for ticker in stocks:
        try:
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers, timeout=10)

            print("Status Code:", response.status_code)
            print("Response Text:", response.text[:200])

            data = response.json()

            if 'quoteResponse' not in data:
                raise Exception("Invalid Yahoo response")

            if len(data['quoteResponse']['result']) == 0:
                raise Exception("No stock data returned")

            result = data['quoteResponse']['result'][0]

            data_list.append({
                "Ticker": ticker,
                "Price": result.get("regularMarketPrice"),
                "Currency": result.get("currency"),
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        except Exception as e:
            data_list.append({
                "Ticker": ticker,
                "Error": str(e)
            })

    latest_data = data_list

    # overwrite latest snapshot
    with open("latest_data.json", "w") as f:
        json.dump(latest_data, f)

    print("Updated latest data")


# -----------------------------
# RUN EVERY 5 MINUTES
# -----------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_stock_data, 'interval', minutes=5)
scheduler.start()

# run once at startup
fetch_stock_data()

# -----------------------------
# API ENDPOINT
# -----------------------------
@app.route('/data')
def get_data():
    return jsonify(latest_data)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)