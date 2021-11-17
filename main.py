import logging
from flask import Flask, render_template,request
import json
import requests

app = Flask(__name__)


@app.route('/')
@app.route('/store')
def home():
    # Cloud function for collecting the product data from mongoDB
    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/collectProducts"
    req = requests.get(url, headers={"Content-type": "application/json", "Accept": "text/plain"})

    return render_template('home.html', products=req.json())

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/ordermanager')
def about():
    return render_template('orderManager.html')

@app.route('/admin')
def form():
    return render_template('admin.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
