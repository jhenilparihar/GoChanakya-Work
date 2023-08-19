from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


def scrape_data():
    today = (datetime.now() - timedelta(1)).strftime("%d-%b-%Y")
    URL = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={today}&todt={today}"
    response = requests.get(f"{URL}")
    data = response.text
    data = data.split("\r\n")
    data_filterd = [i for i in data if i]
    return data_filterd


def getScheme():
    data_filterd = scrape_data()

    keys = [
        "Scheme Code",
        "Scheme Name",
        "ISIN Div",
        "Payout/ISIN Growth",
        "ISIN Div Reinvestment",
        "Net Asset Value",
        "Repurchase Price",
        "Sale Price",
        "Date",
    ]
    x = ""
    y = ""
    list_of_scheme = []

    for i in data_filterd[1:]:
        if "Open Ended Schemes" in i:
            x = i
        elif ";" not in i:
            y = i
        else:
            scheme = {"Fund Name": y, "Category": x}
            for i, j in enumerate(i.split(";")):
                scheme[keys[i]] = j

            list_of_scheme.append(scheme)

    return list_of_scheme


def getPrice():
    data_filterd = scrape_data()

    keys = [
        "Scheme Code",
        "Scheme Name",
        "ISIN Div Payout/ISIN Growth",
        "ISIN Div Reinvestment",
        "Net Asset Value",
        "Repurchase Price",
        "Sale Price",
        "Date",
    ]

    list_of_scheme = []
    for i in data_filterd[1:]:
        if "Open Ended Schemes" in i:
            x = i
        elif ";" not in i:
            y = i
        else:
            scheme = {}
            for i, j in enumerate(i.split(";")):
                if i == 0 or i > 3:
                    if i < 7:
                        if i == 0:
                            scheme[keys[i]] = int(j)
                        elif j != "":
                            scheme[keys[i]] = float(j)
                        else:
                            scheme[keys[i]] = None
                        continue
                    scheme[keys[i]] = j
            list_of_scheme.append(scheme)

    return list_of_scheme


@app.route("/api", methods=["GET"])
def index():
    return jsonify(getPrice())


if __name__ == "__main__":
    app.run()
