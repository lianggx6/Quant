# coding:utf-8
import pandas as pd  # 画图过程中会使用pandas


result_path = r"data_files\results\plot.csv"
df = pd.read_csv(result_path)
print(df.shape)
# df1 = df.loc[df["abs_diff1"] < 20.00]
# print(df1)
print((df["abs_diff2"]*df["abs_diff2"]).mean())


