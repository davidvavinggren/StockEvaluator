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


def get_annual_price(f_dict):
    data = f_dict["historical"]
    annual_price = []
    for i in range(0, len(data), 253):
        annual_price.append(data[i])
        if i == len(data) - len(data) % 365:
            annual_price.append(data[len(data)-1])
    return annual_price


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


def get_dicts(category, label = 0):
    API_SERVER = "https://financialmodelingprep.com/api/v3/"
    url_dict = {"income" : "financials/income-statement/{}".format(label),
                "assets" : "financials/balance-sheet-statement/{}".format(label),
                "financial_ratios" : "financial-ratios/{}".format(label),
                "info" : "company/profile/{}".format(label),
                "key_metrics" : "company-key-metrics/{}?period=quarter".format(label),
                "rating" : "company/rating/{}".format(label),
                "price" : "historical-price-full/{}?serietype=line".format(label),
                "companies" : "company/stock/list"}
    url = API_SERVER + url_dict[category]

    if get_jsn_as_dict(url):
        dict = get_jsn_as_dict(url)
    else:
        print("Stock label not found. Please try again. ")
    return dict


def Main(label):
    f_dicts = {"price" : get_dicts("price", label),
               "income" : get_dicts("income", label),
               "assets" : get_dicts("assets", label),
               "financial_ratios" : get_dicts("financial_ratios", label),
               "info" : get_dicts("info", label),
               "key_metrics" : get_dicts("key_metrics", label),
               "rating" : get_dicts("rating", label),
               "companies" : get_dicts("companies")}
    f_data = {"currency" : "USD",
              "company_name" : f_dicts["info"]["profile"]["companyName"],
              "annual_price" : get_annual_price(f_dicts["price"]),
              "current_price" : f_dicts["info"]["profile"]["price"],
              "description" : f_dicts["info"]["profile"]["description"],
              "website" : f_dicts["info"]["profile"]["website"]}
    label = label.upper()
    plot_graph(f_data["annual_price"],
               f_data["company_name"],
               "annual_stock_price.png",
               " annual stock price",
               "USD", "Time [year]",
               "Value [{}]".format(f_data["currency"]))


Main(sys.argv[1])
