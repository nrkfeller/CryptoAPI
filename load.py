from keras.models import model_from_json
import tensorflow as tf
import h5py


def init(ticker):
    json_file = open('./experiments/model_{}.json'.format(ticker), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    loaded_model.load_weights("./experiments/model_{}.h5".format(ticker))

    loaded_model.compile(loss='mean_squared_error', optimizer='adam')

    graph = tf.get_default_graph()

    return loaded_model, graph
