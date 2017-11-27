import logging

from mongo_repository import MongoCrypto
from flask_pymongo import PyMongo

from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'crypto'
app.config['MONGO_URI'] = \
    'mongodb://nick:bitcoin@ds121456.mlab.com:21456/crypto'
mongo = PyMongo(app)

mc = MongoCrypto(mongo)


@app.route('/train', methods=['GET'])
def add_ticker():
    cryptos = mc.get_stored_cryptos()
    return render_template(
        'add_ticker.html',
        name=cryptos)


@app.route('/train', methods=['POST'])
def submitted_new_crypto():
    ticker = request.form['ticker']

    try:
        mc.save_new_crypto_to_mongo(ticker)
        return render_template(
            'add_ticker.html',
            status="Analyzed Cryptos:",
            name=mc.get_stored_cryptos())
    except:
        return render_template(
            'add_ticker.html',
            status="Count Not Find {}".format(ticker),
            name=mc.get_stored_cryptos())


@app.route('/search')
def form():
    return render_template('form.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():

    searched_crypto = mc.search(request.form['ticker'])

    if not searched_crypto:
        return render_template(
            'submitted_form.html',
            status="Did Not Find",
            name=request.form['ticker'])

    return render_template(
        'submitted_form.html',
        status="Found",
        c=searched_crypto)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
