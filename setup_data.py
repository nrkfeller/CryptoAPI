import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from load import init


def create_dataset(dataset, lookback=1):
    dataX, dataY = [], []
    for i in range(0, len(dataset) - lookback):
        dataY.append(dataset[i + lookback, 0])
        dataX.append(dataset[i])
    return np.array(dataX), np.array(dataY)


def train_test_split(data, test_size=0.2):
    train_set_size = int(len(data) * (1 - test_size))
    train_set = data[:train_set_size]
    test_set = data[-(len(data) - train_set_size):]
    return train_set, test_set


def get_predictions(ds, tiker):

    ds = ds.values.reshape(len(ds), 1)

    scaler = MinMaxScaler(feature_range=(0, 1))

    ds = scaler.fit_transform(ds)

    train, test = train_test_split(ds)

    look_back = 1
    X_train, y_train = create_dataset(train, look_back)
    X_test, y_test = create_dataset(test, look_back)

    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    model, graph = init(tiker)

    with graph.as_default():
        trainPredict = model.predict(X_train)
        testPredict = model.predict(X_test)

    trainPredict = scaler.inverse_transform(trainPredict)
    testPredict = scaler.inverse_transform(testPredict)

    trainPredictPlot = np.empty_like(ds)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(ds)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + 1:len(ds) - 1, :] = testPredict

    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.title("{} Price and Prediction".format(tiker))
    plt.xlabel("Price")
    plt.ylabel("Time")
    b = mpatches.Patch(color='b', label='Historical Price')
    g = mpatches.Patch(color='g', label='Predicted Price')
    plt.legend(handles=[b, g])
    plt.savefig('static/{}.png'.format(tiker))
    plt.clf()

    return list(trainPredict.flatten()), list(testPredict.flatten())
