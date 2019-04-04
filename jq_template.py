# coding: utf-8
import pandas as pd
from datetime import datetime
from jqdatasdk import *

##### 下方代码为 IDE 运行必备代码 #####
if __name__ == '__main__':
    import jqsdk
    params = {
        'token':'4a2661ffb1d8b83c318cd7d4cb22ca23',
        'algorithmId':7,
        'baseCapital':1000000,
        'frequency':'day',
        'startTime':'2019-03-01',
        'endTime':'2019-03-02',
        'name':"Test1",
    }
    jqsdk.run(params)

##### 下面是策略代码编辑部分 #####


def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('initialize run only once')
    run_daily(after_market_close, time='16:00', reference_security='000300.XSHG')

def market_open(context):
    # 输出开盘时间
    log.info('(market_open):' + str(context.current_dt.time()))
    pass


## 收盘后运行函数
def after_market_close(context):
    log.info(str(context.current_dt.time()))
    df = get_price('000001.XSHG', start_date = datetime(1998, 1, 1), end_date = datetime(2019,3,29))
    # df.pop("volume")
    # df.pop("money")
    df['close'].to_csv("SH.csv")
    # df.pop("money")
    print(df)



