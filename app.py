from flask import Flask, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf

app = Flask(__name__)

# --------------------------------
# STOCK LIST
# --------------------------------
stocks = [

    # INDIA
    "ABREL.NS",
    "ACC.NS",
    "AMBUJACEM.NS",
    "ASIANPAINT.NS",

    # USA
    "PHYS",
    "SHY",
    
    # JAPAN
    "8088.T",
    "6310.T",
    "4005.T",
    "6326.T",

    # CURRENCY
    "USDINR=X",
    "JPYINR=X"
]

# --------------------------------
# FETCH LIVE DATA
# --------------------------------
@app.route('/data')
def get_data():

    data_list = []

    for ticker in stocks:

        try:

            stock = yf.Ticker(ticker)

            # Use only fast_info
            fast_info = stock.fast_info

            current_price = fast_info.get("lastPrice")
            previous_close = fast_info.get("previousClose")
            currency = fast_info.get("currency")

            # Skip completely empty responses
            if current_price is None and previous_close is None:
                print(f"Skipping invalid/no-data ticker: {ticker}")
                continue

            data_list.append({

                "Ticker": ticker,

                "CurrentPrice": current_price,

                "PreviousClose": previous_close,

                "Currency": currency,

                "TimeIST": datetime.now(
                    ZoneInfo("Asia/Kolkata")
                ).strftime("%Y-%m-%d %H:%M:%S")

            })

        except Exception as e:

            # IMPORTANT:
            # Don't append error rows to response
            # Just log and continue
            print(f"Error processing {ticker}: {str(e)}")

            continue

    return jsonify(data_list)

# --------------------------------
# HOME
# --------------------------------
@app.route('/')
def home():

    return "Global Market API Running"

# --------------------------------
# MAIN
# --------------------------------
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)