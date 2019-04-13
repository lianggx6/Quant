from util import *


def cost_carry_model_without_bonus():
    result_path = r"data_files\results\cost_carry_model_without_bonus.csv"
    result = integrate_data()

    result["future"] = result["index_price"] + result["index_price"] * \
                       (1 - result["long_rate"]) * result["remaining_days"] / 365 * result["0d_rate"] / 100
    result.to_csv(result_path)
    return result


def cost_carry_model_with_bonus():
    result_path = r"data_files\results\cost_carry_model_with_bonus.csv"
    bonus = calculate_bonus()
    result = cost_carry_model_without_bonus()
    result["future_new"] = result["index_price"] + \
                           result["index_price"] * (1 - result["long_rate"]) * result["remaining_days"] / 365 * result[
                               "0d_rate"] / 100 - \
                           bonus["bonus_ratio"] * result["index_price"]
    result.to_csv(result_path)


if __name__ == "__main__":
    cost_carry_model_with_bonus()
