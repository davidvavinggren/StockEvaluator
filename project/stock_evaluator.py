import requests
import sys
import common
import matplotlib
import matplotlib.pyplot as plt


def get_jsn_as_dict(url):
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


def get_dicts(category, label):
    API_SERVER = "https://financialmodelingprep.com/api/v3/"
    url_dict = {"income" : "financials/income-statement/{}".format(label),
                "assets" : "financials/balance-sheet-statement/{}".format(label),
                "financial_ratios" : "financial-ratios/{}".format(label),
                "info" : "company/profile/{}".format(label),
                "key_metrics" : "company-key-metrics/{}?period=quarter".format(label),
                "rating" : "company/rating/{}".format(label),
                "price" : "historical-price-full/{}?serietype=line".format(label)}
    url = API_SERVER + url_dict[category]

    if get_jsn_as_dict(url):
        dict = get_jsn_as_dict(url)
    else:
        print("Stock label not found. Please try again. ")
    return dict


def Main(label):
    f_dicts = {"price" : get_dicts("price", label),
               "income" : get_data("income", label),
               "assets" : get_data("assets", label),
               "financial_ratios" : get_data("financial_ratios", label),
               "info" : get_data("info", label),
               "key_metrics" : get_data("key_metrics", label),
               "rating" : get_data("rating", label)}
    f_data = {""}
    currency = "USD"
    company_name = f_dicts["info"]["profile"]["companyName"]
    label = label.upper()
    period_annual = get_period_annual(f_dicts["price"])
    plot_graph(period_annual,
               company_name,
               "annual_stock_price.png",
               " annual stock price",
               "USD", "Time [year]",
               "Value [" + currency + "]")


Main(sys.argv[1])
