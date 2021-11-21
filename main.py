import logging
from flask import Flask, render_template,request, session
import json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '6ccdb527e50c20c5deb736d0d090f584'

@app.route('/', methods = ['POST','GET'])
@app.route('/store', methods = ['POST','GET'])
def home():
    # Cloud function for collecting the product data from mongoDB
    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/collectProducts"
    req = requests.get(url, headers={"Content-type": "application/json", "Accept": "text/plain"})

    if request.method == 'POST':
        if "buy" in request.form:
            quantity = request.form.get('amount')
            productID = request.form.get('productID')
            print(quantity)
            print(productID)

            basketItem = {'productID':productID, 'quantity':quantity}

            if not session.get("basket") is None:
                session['basket'] = session['basket'].extend([basketItem])
                print("here")
            else:
                session['basket'] = [basketItem]
                print("there")

    return render_template('home.html', products=req.json())

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')#, basket = session['basket'])

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
