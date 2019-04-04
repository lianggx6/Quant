# coding:utf-8
import matplotlib.pyplot as plt  # 为方便简介为plt
import pandas as pd  # 画图过程中会使用pandas

from IPython.core.pylabtools import figsize

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
df1 = pd.read_csv("HS300_pre.csv", index_col=0)
df2 = pd.read_csv("HS300_None.csv", index_col=0)
df1["return"] = df2.loc[df2["price"] > 9.0]
df1.index = pd.to_datetime(df1.index)

figsize(100, 20)

plt.plot(df1.index, df1["price"], label="上证")
plt.legend(loc=2)
plt.twinx()
plt.bar(df1.index, df1["return"], color="red", label="ZQ")
plt.ylim((0, 5))
plt.legend(loc=1)
plt.show()
