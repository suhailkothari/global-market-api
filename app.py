from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import yfinance as yf
import json

app = Flask(__name__)

# --------------------------------
# STOCK LIST
# --------------------------------
stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "7203.T",
    "6758.T",
    "AAPL",
    "MSFT"
]

latest_data = []

# --------------------------------
# FETCH STOCK DATA
# --------------------------------
def fetch_stock_data():
    global latest_data

    data_list = []

    for ticker in stocks:
        try:

            stock = yf.Ticker(ticker)

            # fetch latest fast info
            info = stock.fast_info

            data_list.append({
                "Ticker": ticker,
                "Price": info.get("lastPrice"),
                "Currency": info.get("currency"),
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

    print("Latest stock data updated")


# --------------------------------
# RUN EVERY 5 MINUTES
# --------------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_stock_data, 'interval', minutes=5)
scheduler.start()

# run once immediately
fetch_stock_data()

# --------------------------------
# API ENDPOINT
# --------------------------------
@app.route('/data')
def get_data():
    return jsonify(latest_data)

# --------------------------------
# MAIN
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)