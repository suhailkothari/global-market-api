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
    "INDIGRID-IV.NS",
    "PGINVIT-IV.NS",
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
    
    # USA
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

    # JAPAN
    "8088.T",
    "6310.T",
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

            fast_info = stock.fast_info

            hist = stock.history(period="2d")

            previous_close = None

            if len(hist) > 1:
                previous_close = float(hist["Close"].iloc[-2])

            current_price = fast_info.get("lastPrice")

            currency = fast_info.get("currency")

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

            data_list.append({

                "Ticker": ticker,

                "Error": str(e),

                "TimeIST": datetime.now(
                    ZoneInfo("Asia/Kolkata")
                ).strftime("%Y-%m-%d %H:%M:%S")

            })

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