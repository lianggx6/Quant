import wget
from jqdatasdk import *
from datetime import datetime, timedelta
import pandas as pd
import json


def get_hs300_index():
    df = get_price("000300.XSHG", start_date="2011-01-01", end_date="2019-01-01", fq=None)
    df.to_csv(r"data_files\HS300_None.csv")


def get_hs300_future():
    info = pd.read_csv(r"data_files\future\hs300_future_info.csv", index_col=0)
    for contract in info["name"]:
        df = get_price(contract + ".CCFX", start_date="2011-01-01", end_date="2019-01-01", fq=None)
        df.to_csv(r"data_files\future\%s.csv" % contract)


def get_future_info():
    df = get_all_securities(types=['futures'])
    df.to_csv(r"data_files\future\info.csv", encoding="gbk")


def get_hs300_stock_info():
    path = r"data_files\stock\hs300_stocks.json"
    stocks = {}
    for year in range(2011, 2019):
        first = "%d-03-01" % year
        second = "%d-09-01" % year
        stocks[first] = get_index_stocks('000300.XSHG', first)
        stocks[second] = get_index_stocks('000300.XSHG', second)
    with open(path, "w") as f:
        json.dump(stocks, f)


def get_hs300_stock_quote():
    code_path = r"data_files\stock\hs300_stocks.json"
    store_path = r"data_files\stock\quote\%s.csv"
    with open(code_path, "r") as f:
        stocks = json.load(f)
    stock_set = set()
    for value in stocks.values():
        stock_set.update(value)
    for stock in stock_set:
        df = get_price(stock, start_date="2011-01-01", end_date="2019-01-01", fq=None)
        df.to_csv(store_path % stock)


def get_hs300_stock_bonus():
    code_path = r"data_files\stock\hs300_stocks.json"
    store_path = r"data_files\stock\bonus\%s.csv"
    with open(code_path, "r") as f:
        stocks = json.load(f)
    stock_set = set()
    for value in stocks.values():
        stock_set.update(value)
    for stock in stock_set:
        q = query(finance.STK_XR_XD). \
            filter(finance.STK_XR_XD.code == stock,
                   finance.STK_XR_XD.report_date >= '2010-01-01',
                   finance.STK_XR_XD.report_date <= '2019-01-01'). \
            order_by(finance.STK_XR_XD.report_date)
        df = finance.run_query(q)
        df.to_csv(store_path % stock)


def get_hs300_stock_valuation():
    code_path = r"data_files\stock\hs300_stocks.json"
    store_path = r"data_files\stock\value\%s.csv"
    with open(code_path, "r") as f:
        stocks = json.load(f)
    stock_set = set()
    for value in stocks.values():
        stock_set.update(value)
    for stock in stock_set:
        if stock.startswith("60"):
            q = query(valuation.market_cap).filter(valuation.code == stock)
            panel = get_fundamentals_continuously(q, end_date="2019-01-01", count=8 * 250)
            df = panel.minor_xs(stock)
            df.to_csv(store_path % stock)


def get_hs300_index_info():
    store_path = r"data_files\index\weight\%s.csv"
    code_path = r"data_files\index\HS300_index.csv"
    index = pd.read_csv(code_path, index_col=0)
    for date in index.index:
        df = get_index_weights("000300.XSHG", date)
        df.to_csv(store_path % date)


def get_hs300_future_price():
    info_path = r"data_files\future\hs300_future_info.csv"
    store_path = r"data_files\future\settle\settle.csv"
    info = pd.read_csv(info_path, index_col=0)
    df = get_extras('futures_sett_price', list(info.index), start_date='2011-01-01', end_date='2019-01-01', df=True)
    df.to_csv(store_path)


def get_settle_param():
    base_url = r"http://www.cffex.com.cn/sj/jscs/%s/%s/%s_1.csv"
    start_date = datetime(2011, 1, 1)
    end_date = datetime(2019, 1, 1)
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        url = base_url % (date.strftime("%Y%m"), date.strftime("%d"), date.strftime("%Y%m%d"))
        store_path = r"data_files\future\param\%s.csv" % date.strftime("%Y%m%d")
        # try:
        wget.download(url, store_path)
        # except Exception as err:
        #     print(err)


def get_remain():
    print(get_query_count())


if __name__ == "__main__":
    auth("15066299571", "jiayouLGX,1996.")
    get_hs300_future()
    # get_future_info()
    # get_hs300_index()
    # get_hs300_stock_info()
    # get_hs300_stock_quote()
    # get_hs300_stock_bonus()
    # get_hs300_stock_valuation()
    # get_hs300_index_info()
    # get_hs300_future_price()
    # get_settle_param()

    get_remain()
