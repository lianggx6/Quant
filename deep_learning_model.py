from tensorflow.python.keras.utils import normalize
from tensorflow.python.keras import *
from util import *
import numpy as np
import tensorflow as tf

index_max = 5380.43
index_min = 2023.17


def normalize_index(seq):
    return (seq - index_min) / (index_max - index_min)


def re_normalize_index(seq):
    return seq * (index_max - index_min) + index_min


def load_data():
    rate_train_data = []
    quote_train_data = []
    dense_train_data = []
    train_labels = []

    rate_test_data = []
    quote_test_data = []
    dense_test_data = []
    test_labels = []

    result = pd.read_csv(r"data_files\results\integrate_date.csv", index_col=0)
    bonus = pd.read_csv(r"data_files\results\bonus.csv", index_col=0)

    result["close"] = normalize_index(result["close"])
    result["high"] = normalize_index(result["high"])
    result["low"] = normalize_index(result["low"])
    result["open"] = normalize_index(result["open"])
    result["volume"] = normalize(np.array(result["volume"]))[0]
    result["money"] = normalize(np.array(result["money"]))[0]
    result["remaining_days"] = normalize(np.array(result["remaining_days"]))[0]
    result["settle_price"] = normalize(np.array(result["settle_price"]))[0]
    bonus["bonus_ratio"] = normalize(np.array(bonus["bonus_ratio"]))[0]

    for term in ["0d", "1m", "3m", "6m", "9m", "1y"]:
        result[term] = normalize(np.array(result[term]))[0]
    for date in result.index:
        if date < "2011-02-01":
            continue
        df = result.iloc[result.index <= date].tail(20)
        quote_sample = np.array([df["open"], df["close"], df["high"], df["low"], df["volume"], df["money"]]).T
        rate_sample = np.array([df["0d"], df["1m"], df["3m"], df["6m"], df["9m"], df["1y"]]).T
        if date < "2018-01-01":
            quote_train_data.append(quote_sample)
            rate_train_data.append(rate_sample)
            dense_train_data.append(np.array([df.loc[date, "remaining_days"],
                                              df.loc[date, "long_rate"], bonus.loc[date, "bonus_ratio"]]))
            train_labels.append(df.loc[date, "settle_price"])
        else:
            quote_test_data.append(quote_sample)
            rate_test_data.append(rate_sample)
            dense_test_data.append(np.array([df.loc[date, "remaining_days"],
                                             df.loc[date, "long_rate"], bonus.loc[date, "bonus_ratio"]]))
            test_labels.append(df.loc[date, "settle_price"])

    quote_train_data = np.array(quote_train_data)
    rate_train_data = np.array(rate_train_data)
    dense_train_data = np.array(dense_train_data)
    train_labels = np.array(train_labels)

    quote_test_data = np.array(quote_test_data)
    rate_test_data = np.array(rate_test_data)
    dense_test_data = np.array(dense_test_data)
    test_labels = np.array(test_labels)
    return (quote_train_data, rate_train_data, dense_train_data, train_labels), \
           (quote_test_data, rate_test_data, dense_test_data, test_labels)


def training(train_data, test_data):
    quote_input = Input(shape=(20, 6))
    rate_input = Input(shape=(20, 6))
    dense_input = Input(shape=(3,))

    quote_layer1 = layers.CuDNNLSTM(60)(quote_input)
    rate_layer1 = layers.CuDNNLSTM(60)(rate_input)

    full_input = layers.concatenate([quote_layer1, rate_layer1, dense_input])
    dense_layer1 = layers.Dense(10, activation=tf.nn.relu)(full_input)
    drop_layer = layers.Dropout(0.1)(dense_layer1)
    prediction = layers.Dense(1, activation=tf.nn.softmax)(drop_layer)

    model = Model(inputs=[quote_input, rate_input, dense_input], outputs=prediction)
    model.compile(optimizer=tf.train.AdamOptimizer(0.001),
                  loss=losses.mse,
                  metrics=[metrics.mse])

    model.fit([train_data[0], train_data[1], train_data[2]], train_data[3], epochs=50,
              callbacks=[callbacks.TensorBoard(log_dir='./logs')])


if __name__ == "__main__":
    train, test = load_data()
    print("---------------------------load data end--------------------------")
    training(train, test)
