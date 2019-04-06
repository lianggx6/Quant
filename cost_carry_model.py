import os
import pandas as pd


def integrate_data():
    hs300_path = r"data_files\index\hs300_index.csv"
    rate_path = r"data_files\rate\%s.csv"
    param_path = r"data_files\future\param"
    future_path = r"data_files\future\hs300_future_info.csv"
    settle_path = r"data_files\future\settle\settle.csv"
    future_quote_path = r"data_files\future\quote\%s.csv"
    hs300 = pd.read_csv(hs300_path, index_col=0)
    future_info = pd.read_csv(future_path, index_col=0)
    settle = pd.read_csv(settle_path, index_col=0)
    result = pd.DataFrame()
    hs300 = hs300.loc[hs300.index >= "2018-01-01"]
    result["index_price"] = hs300["close"]
    result.index = hs300.index
    for date in hs300.index:
        rates = pd.read_csv(rate_path % date, index_col=0)
        param_files = pd.Series(os.listdir(param_path))
        params = pd.read_csv(os.path.join(param_path, param_files[param_files <= date + ".csv"].iloc[-1]), index_col=0)
        result.loc[date, "main_contract"] = future_info.loc[future_info["end_date"] >= date]["name"][0]
        result.loc[date, "end_date"] = future_info.loc[future_info["end_date"] >= date]["end_date"][0]
        result.loc[date, "long_rate"] = params.loc[params["name"] == result.loc[date, "main_contract"]]["long_rate"][0]
        result.loc[date, "0d_rate"] = rates.loc[rates["term"] == "0d"]["rate"][0]
        result.loc[date, "1m_rate"] = rates.loc[rates["term"] == "1m"]["rate"][0]
        result.loc[date, "settle_price"] = settle.loc[date, result.loc[date, "main_contract"]]
        result.loc[date, "close_price"] = pd.read_csv(future_quote_path % result.loc[date, "main_contract"], index_col=0).loc[date, "close"]
    return result


def cost_carry_model_without_bonus():
    result_path = r"data_files\results\cost_carry_model_without_bonus.csv"
    result = integrate_data()
    result["remaining_days"] = pd.to_datetime(result["end_date"]) - pd.to_datetime(result.index)
    result["remaining_days"] = result["remaining_days"].apply(lambda x: x.days)
    result["future"] = result["index_price"] + result["index_price"]*(1-result["long_rate"])*result["remaining_days"]/365*result["0d_rate"]/100
    result.to_csv(result_path)
    print(result)


def cost_carry_model_with_bonus():
    pass


if __name__ == "__main__":
    cost_carry_model_without_bonus()
