import os

import pandas as pd


def integrate_data(start_date, end_date="2019-01-01"):
    hs300_path = r"data_files\single_files\hs300_index.csv"
    rate_path = r"data_files\rate\%s.csv"
    param_path = r"data_files\param"
    future_path = r"data_files\single_files\hs300_future.csv"
    settle_path = r"data_files\single_files\future_settle.csv"
    hs300 = pd.read_csv(hs300_path, index_col=0)
    future_info = pd.read_csv(future_path, index_col=0)
    settle = pd.read_csv(settle_path, index_col=0)
    hs300 = hs300.loc[(hs300.index >= start_date) & (hs300.index <= end_date)]
    result = hs300
    for date in hs300.index:
        rates = pd.read_csv(rate_path % date, index_col=0)
        param_files = pd.Series(os.listdir(param_path))
        params = pd.read_csv(os.path.join(param_path, param_files[param_files <= date + ".csv"].iloc[-1]), index_col=0)
        result.loc[date, "main_contract"] = future_info.loc[future_info["end_date"] >= date]["name"][0]
        result.loc[date, "end_date"] = future_info.loc[future_info["end_date"] >= date]["end_date"][0]
        result.loc[date, "long_rate"] = params.loc[params["name"] == result.loc[date, "main_contract"]]["long_rate"][0]
        result.loc[date, "settle_price"] = settle.loc[date, result.loc[date, "main_contract"]]
        result["remaining_days"] = pd.to_datetime(result["end_date"]) - pd.to_datetime(result.index)
        result["remaining_days"] = result["remaining_days"].apply(lambda x: x.days)
        for term in ["0d", "1m", "3m", "6m", "9m", "1y"]:
            result.loc[date, term] = rates.loc[rates["term"] == term]["rate"][0]
    return result


def calculate_bonus(start_date):
    hs300_path = r"data_files\single_files\hs300_index.csv"
    weight_path = r"data_files\weight\%s.csv"
    bonus_path = r"data_files\bonus"
    result_path = r"data_files\results\bonus.csv"
    hs300 = pd.read_csv(hs300_path, index_col=0)
    hs300 = hs300.loc[hs300.index >= start_date]
    bonus_ratio = pd.DataFrame()
    for date in hs300.index:
        bonus_ratio.loc[date, "bonus_ratio"] = 0.0
        if date + ".csv" not in os.listdir(bonus_path):
            continue
        weight = pd.read_csv(weight_path % date, index_col=0)
        bonus = pd.read_csv(os.path.join(bonus_path, date + ".csv"), index_col=0)
        for stock in weight.index:
            if stock in bonus.index:
                bonus_ratio.loc[date, "bonus_ratio"] += \
                    bonus.loc[stock, "bonus_amount_rmb"] / weight.loc[stock, "market_cap"] * \
                    weight.loc[stock, "weight"] / 1000000
    bonus_ratio.to_csv(result_path)
    return bonus_ratio


if __name__ == "__main__":
    # result_path = r"data_files\results\integrate_date.csv"
    # result = integrate_data("2011-01-01")
    # result.to_csv(result_path)
    calculate_bonus("2011-01-01")
