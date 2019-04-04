import os
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
        df["date"] = df["date"].apply(lambda x:datetime.strptime(x, "%Y/%m/%d"))
        df.to_csv(fp)


def process_param():
    base_path = r"data_files\future\param"
    for fp in os.listdir(base_path):
        if(os.path.getsize(os.path.join(base_path, fp))) == 2132:
            os.remove(os.path.join(base_path, fp))


if __name__ == "__main__":
    # process_date()
    process_param()
