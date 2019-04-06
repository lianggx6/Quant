import os
import re
from datetime import datetime

import pandas as pd


def process_hs300_weight():
    code_path = r"index_row.csv"
    info_path = r"data_files\index\HS300_index.csv"
    store_path = r"data_files\temp\%s.csv"
    index = pd.read_csv(info_path, index_col=0)
    df = pd.read_csv(code_path)
    for date in index.index:
        if date < "2012/1/1":
            date_t = datetime.strptime(date, "%Y-%m-%d")
            date_t = "%d/%d/%d" % (date_t.year, date_t.month, date_t.day)
            df_temp = df.loc[df["Enddt"] == date_t]
            df_save = df_temp.drop(["Indexcd"], axis=1)
            df_save.columns = ["date", "code", "display_name", "weight"]
            df_save["code"] = df_save["code"].apply(lambda x: str(x).zfill(6) + ".XSHG"
            if str(x).startswith("60") else str(x).zfill(6) + ".XSHE")
            df_save.insert(2, "date", df_save.pop("date"))
            df_save.to_csv(store_path % date, index=None)
        else:
            break


def process_date():
    path = r"data_files\index\weight"
    for fp in os.listdir(path):
        fp = os.path.join(path, fp)
        df = pd.read_csv(fp)
        df["date"] = df["date"].apply(lambda x: datetime.strptime(x, "%Y/%m/%d"))
        df.to_csv(fp)


def process_param1():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        if (os.path.getsize(os.path.join(base_path, fp))) == 2132:
            os.remove(os.path.join(base_path, fp))


def process_param2():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        df = pd.read_csv(file_path, encoding="gbk")
        df.to_csv(file_path, header=None)


def process_param3():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        df = pd.read_csv(file_path)
        df.columns = ["name", "long_rate", "short_rate", "trade_rate", "settle_rate", "close_rate"]
        df["name"] = df["name"].apply(lambda x: x.strip())
        df.index = df["name"].map(lambda x: x + ".CCFX")
        df.index.name = None
        df = df.loc[df["name"].str.startswith("IF")]
        df.to_csv(file_path)


def process_param4():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        df = pd.read_csv(file_path)
        if len(df["close_rate"][2]) > 5 and df["close_rate"][2] != "10000%":
            print(fp)


def process_param5():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        df = pd.read_csv(file_path, index_col=0)
        df["long_rate"] = df["long_rate"].apply(lambda x: float(x.replace("%", "")) / 100)
        df["short_rate"] = df["short_rate"].apply(lambda x: float(x.replace("%", "")) / 100)
        df["close_rate"] = df["close_rate"].apply(lambda x: float(x.replace("%", "")) / 100)
        df["trade_rate"] = df["trade_rate"].apply(lambda x: float(re.search(r"\d+(\.\d+)?", x).group(0)) / 10000)
        df["settle_rate"] = df["settle_rate"].apply(lambda x: float(re.search(r"\d+(\.\d+)?", x).group(0)) / 10000)
        df.to_csv(file_path)


def process_param6():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        new_fp = datetime.strptime(fp[:8], "%Y%m%d").strftime("%Y-%m-%d.csv")
        os.rename(file_path, os.path.join(base_path, new_fp))


def process_rate1():
    base_path = r"data_files\rate"
    rates = pd.DataFrame()
    for fp in os.listdir(base_path):
        file_path = os.path.join(base_path, fp)
        df = pd.read_csv(file_path)
        rates = rates.append(df, sort=False)
    rates.to_csv(os.path.join(base_path, "rates.csv"))


def process_rate2():
    row_path = r"data_files\rate\rates.csv"
    info_path = r"data_files\index\HS300_index.csv"
    store_path = r"data_files\rate\%s.csv"
    index = pd.read_csv(info_path, index_col=0)
    rates = pd.read_csv(row_path, index_col=0)
    rates.index = pd.to_datetime(rates.index)
    for date in index.index:
        df = rates.loc[rates.index == date]
        df.to_csv(store_path % date)


def process_future_info_date():
    future_path = r"data_files\future\hs300_future_info.csv"
    df = pd.read_csv(future_path, index_col=0)
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    df.to_csv(future_path)


def process_settle():
    settle_path = r"data_files\future\settle\settle.csv"
    df = pd.read_csv(settle_path, index_col=0)
    df.columns = map(lambda x: x[:6], df.columns)
    df.to_csv(settle_path)
    print(df)


def process_future_quote():
    quote_path = r"data_files\future\quote"
    info_path = r"data_files\index\HS300_index.csv"
    store_path = r"data_files\temp\%s.csv"
    info = pd.read_csv(info_path, index_col=0)
    for date in info.index:
        df = pd.DataFrame()
        index_list = []
        for quote_file in os.listdir(quote_path):
            quote_file_path = os.path.join(quote_path, quote_file)
            df_t = pd.read_csv(quote_file_path, index_col=0)
            df_t = df_t.loc[(df_t.index == date) & (df_t["close"].notnull())]
            if not df_t.empty:
                df = df.append(df_t.loc[df_t.index == date], ignore_index=True)
                index_list.append(quote_file[:6])
        df.index = index_list
        df.to_csv(store_path % date)


def process_bonus1():
    info_path = r"data_files\index\HS300_index.csv"
    bonus_path = r"data_files\stock\bonus"
    store_path = r"data_files\temp\%s.csv"
    info = pd.read_csv(info_path, index_col=0)
    for date in info.index:
        if date < "2018-06-07":
            continue
        df = pd.DataFrame()
        index_list = []
        print(date)
        for bonus_file in os.listdir(bonus_path):
            bonus_file_path = os.path.join(bonus_path, bonus_file)
            df_t = pd.read_csv(bonus_file_path, index_col=0)
            df_t = df_t.loc[df_t["a_bonus_date"] == date]
            if not df_t.empty:
                df = df.append(df_t)
                index_list.append(bonus_file[:6])
        try:
            df.index = index_list
        except ValueError:
            print(index_list)
            break
        df = df.dropna(1)
        if not df.empty:
            df.to_csv(store_path % date)


def process_bonus2():
    pass


if __name__ == "__main__":
    # process_date()
    # process_param2()
    # process_param3()
    # process_param4()
    # process_rate1()
    # process_rate2()
    # process_param5()
    # process_future_info_date()
    # process_param6()
    # process_settle()
    # process_future_quote()
    process_bonus1()
