import requests
import json

URL = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt=20-Jun-2023&todt=20-Jun-2023"
response = requests.get(f"{URL}")
data = response.text
data = data.split("\r\n")
data_filterd = [i for i in data if i]

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


file_path = "schemes.json"
file_ = open(file_path, "w")
json.dump(list_of_scheme, file_)
