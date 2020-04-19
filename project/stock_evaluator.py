import requests
import sys
import common
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf


API_SERVER = "https://financialmodelingprep.com/api/v3/"

#https://financialmodelingprep.com/api/v3/financials/income-statement/AAPL
#https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/AAPL
#https://financialmodelingprep.com/api/v3/financial-ratios/AAPL
#https://financialmodelingprep.com/api/v3/company/profile/AAPL
#https://financialmodelingprep.com/api/v3/quote/AAPL,FB
#https://financialmodelingprep.com/api/v3/company-key-metrics/AAPL?period=quarter
#https://financialmodelingprep.com/api/v3/company/rating/AAPL
#https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?serietype=line

def get_jsn_as_dict(stock_label):
    url = (API_SERVER
           + "historical-price-full/"
           + stock_label
           + "?serietype=line")
    uerel = requests.get(url)
    uerel_json = uerel.json()
    if uerel.status_code == 200:
        return uerel_json
    else:
        print("ERROR")


def get_period_annual(f_dict):
    data = f_dict["historical"]
    period_annual = []
    for i in range(0, len(data), 253):
        period_annual.append(data[i])
        if i == len(data) - len(data) % 365:
            period_annual.append(data[len(data)-1])
    return period_annual


def plot_graph(list, company_name, plot_name = 0, plot_title = 0,
               currency = 0, x_label = 0, y_label = 0):
    x_values = []
    y_values = []
    #step_length =
    for element in list:
        x_values.append(element["date"][2:4])
        y_values.append(element["close"])
    plt.figure()
    plt.plot(x_values, y_values)
    plt.xticks(x_values[0:len(list):2] + [x_values[len(list)-1]])
    plt.title(company_name + plot_title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(plot_name)


def Main(label):
    currency = "USD"
    company = yf.Ticker(label)
    company_name = company.info["longName"]
    stock_label = label.upper()
    if get_jsn_as_dict(stock_label):
        f_history = get_jsn_as_dict(stock_label)
    else:
        print("Stock label not found. Please try again. ")
        return
    period_annual = get_period_annual(f_history)
    plot_graph(period_annual,
               company_name,
               "annual_closing_price.png",
               " annual closing price",
               "USD", "Time [year]",
               "Value [" + currency + "]")



Main(sys.argv[1])
