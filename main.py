import logging
from flask import Flask, render_template,request, session, url_for, redirect
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

    return render_template('home.html', products=req.json())

# User Checkout
@app.route('/checkout')
def checkout():
    if(request.cookies.get("token")):
        return render_template('checkout.html')
    else:
        return redirect(url_for('home'))

# Admin Order Manager
@app.route('/ordermanager')
def orderManager():

    # Get all order information

    return render_template('orderManager.html', role="admin")

# Admin Order Manager (Single order)
@app.route('/ordermanager/<orderNumber>')
def orderView(orderNumber):

    # Cloud function to get order details using 'orderNumber'

    return render_template('orderView.html', role="admin")

# User Order History
@app.route('/orderhistory')
def orderHistory():

    # Get all order information

    return render_template('orderManager.html', role="user")

# User Order History (Single Order)
@app.route('/orderhistory/<orderNumber>')
def orderHistoryView(orderNumber):

    # Cloud function to get order details using 'orderNumber'

    return render_template('orderView.html', role="user")

# Admin Controls
@app.route('/admin')
def form():
    return render_template('admin.html')

# 500 Error response
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# 404 Error Response
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.context_processor
def injectGlobals():
    userData = authenticate()
    return dict(token=userData[0], name=userData[1])

def authenticate():
    authToken = request.cookies.get("token")
    userRole = request.cookies.get("name")
    return [authToken, userRole]

if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
