import requests
import pandas
from matplotlib import pyplot
import numpy as np
from bs4 import BeautifulSoup

URLS = {
    "Privat_bank": "https://minfin.com.ua/company/privatbank/currency/",
    "Alfa_bank": "https://minfin.com.ua/company/alfa-bank/currency/",
    "Oschad_bank": "https://minfin.com.ua/company/oschadbank/currency/"
}


def main():
    write_data()
    # result = pandas.read_csv("Privat_bankExchange.csv", header=0)
    # result.plot()
    #
    # pyplot.show()


def parse(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    rs = soup.find(class_="currency-data")
    try:
        temp = rs.tbody.tr.contents
    except Exception:
        return
    value = temp[3].contents

    return value[0]



def create_dict(bank_url):
    dic = {"Date": [], "usd": []}
    for j in range(1, 10):
        date = f"2020-09-0{j}"
        url = f'{bank_url}{date}/'
        text = parse(url)
        if text is None:
            continue
        text = process_data(text)
        dic["Date"].append(date)
        dic["usd"].append(text)

    return dic



def process_data(text):
    text = text.strip()
    return text



def write_data():
    for key, value in URLS.items():
        dic = create_dict(value)
        arr = pandas.DataFrame(data=dic)
        arr.to_csv(f"{key}Exchange.csv", index=False)



if __name__ == "__main__":
    main()