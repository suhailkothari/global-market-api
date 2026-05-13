from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
import json

app = Flask(__name__)

# --------------------------------
# STOCK LIST
# --------------------------------
stocks = [
    "ABREL.NS",
    "ACC.NS",
    "AMBUJACEM.NS",
    "ASIANPAINT.NS",
    "BANKBARODA.NS",
    "BRIGADE.NS",
    "CANBK.NS",
    "COALINDIA.NS",
    "CONCOR.NS",
    "EICHERMOT.NS",
    "GODREJPROP.NS",
    "GPPL.NS",
    "HDFCBANK.NS",
    "HINDALCO.NS",
    "HINDCOPPER.NS",
    "HINDZINC.NS",
    "IEX.NS",
    "INOXINDIA.NS",
    "ITC.NS",
    "JIOFIN.NS",
    "KANSAINER.NS",
    "KOTAKBANK.NS",
    "MIDHANI.NS",
    "NLCINDIA.NS",
    "NTPC.NS",
    "OBEROIRLTY.NS",
    "ONGC.NS",
    "PNB.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBIN.NS",
    "SEAMECLTD.NS",
    "SUNTECK.NS",
    "TATACHEM.NS",
    "TATACOMM.NS",
    "TATAPOWER.NS",
    "TATASTEEL.NS",
    "TCS.NS",
    "TMCV.NS",
    "TMPV.NS",
    "WIPRO.NS",
    "BANKBEES.NS",
    "FMCGIETF.NS",
    "NIFTYBEES.NS",
    "HNGSNGBEES.NS",
    "LIQUIDBEES.NS",
    "LIQUIDCASE.NS",
    "SETF10GILT.NS",
    "EBBETF0431.NS",
    "EBBETF0433.NS",
    "GOLDBEES.NS",
    "SILVERBEES.NS",
    "540565.BO",
    "543290.BO",
    "PHYS",
    "SHY",
    "IEI",
    "AMAT",
    "APD",
    "BABA",
    "BIDU",
    "BMNR",
    "CC",
    "NVO",
    "NTR",
    "XRT",
    "XLE",
    "XLI",
    "DAX",
    "EWJ",
    "EWZ",
    "KTEC",
    "EUAD",
    "CHIQ",
    "ILIT",
    "COPX",
    "GDX",
    "PALL",
    "URNM",
    "SIL",
    "8088.T",
    "6310.T",
    "6326.T",
    "USDINR=X",
    "JPYINR=X"
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

            # Fast latest data
            info = stock.fast_info

            data_list.append({
                "Ticker": ticker,
                "CurrentPrice": info.get("lastPrice"),
                "PreviousClose": stock.history(period="2d")["Close"].iloc[-2] if len(stock.history(period="2d")) > 1 else None,
                "Currency": info.get("currency"),
                "TimeIST": datetime.now(
                    ZoneInfo("Asia/Kolkata")
                ).strftime("%Y-%m-%d %H:%M:%S")
            })

        except Exception as e:

            data_list.append({
                "Ticker": ticker,
                "Error": str(e),
                "TimeIST": datetime.now(
                    ZoneInfo("Asia/Kolkata")
                ).strftime("%Y-%m-%d %H:%M:%S")
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

# run immediately at startup
fetch_stock_data()

# --------------------------------
# API ENDPOINT
# --------------------------------
@app.route('/data')
def get_data():
    return jsonify(latest_data)

# --------------------------------
# HOME ROUTE
# --------------------------------
@app.route('/')
def home():
    return "Global Market API Running"

# --------------------------------
# MAIN
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)