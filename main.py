import requests
import pandas
from matplotlib import pyplot
import numpy as np
from bs4 import BeautifulSoup
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error


URLS = {
    "Privat": "https://minfin.com.ua/company/privatbank/currency/",
    "Alfa_bank": "https://minfin.com.ua/company/alfa-bank/currency/",
    "Oschad": "https://minfin.com.ua/company/oschadbank/currency/"
}

SEARCHED_DATE = "2020-09"
COUNT_DAYS = 30


def main():

    # write_data()

    ActualData = pandas.read_csv("PrivatExchange.csv", header=0, parse_dates=[0], index_col=0).values
    NumberofElements = len(ActualData)

    #Use 70% of data as training, rest 30% Test model
    TrainingSize = int(NumberofElements * 0.7)
    TrainingData = ActualData[0:TrainingSize]
    TestData = ActualData[TrainingSize:NumberofElements]

    Actual = [x for x in TrainingData]
    Predictions = list()

    for timepoint in range(len(TestData)):
        ActualValue = TestData[timepoint]
        Prediction = StartArimaForecasting(Actual, 3, 1, 0)

        Predictions.append(Prediction)
        Actual.append(ActualValue)


    Error = mean_squared_error(TestData, Predictions)

    print(Error)

    pyplot.plot(TestData)
    pyplot.plot(Predictions, color="red")
    pyplot.show()


    # while(True):
    #     print("Exit - exit")
    #     response = input("Do you want to draw graphic? :> ")
    #     if response.lower() == "exit":
    #         return
    #     if response.lower() == "yes" or response.lower() == "y":
    #         bank_name = input("Enter a bank name(Privat, Alfa-bank, Oschad :> ")
    #         bank_name = bank_name.replace('-', '_')
    #         if bank_name not in URLS.keys():
    #             print("The bank not exists")
    #             continue
    #         bank_name = f"{bank_name}Exchange.csv"
    #
    #         draw_graphic(bank_name)


def write_data():
    for key, value in URLS.items():
        dic = create_dict(value)
        arr = pandas.DataFrame(data=dic)
        arr.to_csv(f"{key}Exchange.csv", index=False)


def draw_graphic(filename):
    df = pandas.read_csv(f"{filename}", header=0)
    df.plot()
    pyplot.show()


def create_dict(bank_url):
    dic = {"Date": [], "usd": []}

    for j in range(1, COUNT_DAYS + 1):

        date = f"{SEARCHED_DATE}-{j}" if j >= 10 else f"{SEARCHED_DATE}-0{j}"
        url = f'{bank_url}{date}/'
        text = parse(url)
        print(f"Parsing pages - {j}")
        if text is None:
            continue
        text = process_data(text)
        dic["Date"].append(date)
        dic["usd"].append(text)

    return dic


def parse(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    rs = soup.find(class_="currency-data")
    try:
        temp = rs.tbody.tr.contents
    except Exception as e:
        return
    value = temp[3].contents

    return value[0]


def process_data(text):
    text = text.strip()
    return text


def StartArimaForecasting(Actual, P, D, Q):
    model = ARIMA(Actual, order=(P, D, Q))
    model_fit = model.fit(disp=0)
    prediction = model_fit.forecast()[0]
    return prediction


if __name__ == "__main__":
    main()