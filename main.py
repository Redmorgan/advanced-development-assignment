import logging
from flask import Flask, render_template, request, session, url_for, redirect
import json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '6ccdb527e50c20c5deb736d0d090f584'


@app.route('/', methods=['POST', 'GET'])
@app.route('/store', methods=['POST', 'GET'])
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
    if session['userRole'] == "admin":

        return render_template('orderManager.html', pageType="admin")

    else:

        return redirect(url_for('home'))


# Admin Order Manager (Single order)
@app.route('/ordermanager/<orderNumber>')
def orderView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if session['userRole'] == "admin":

        return render_template('orderView.html', pageType="admin")

    else:

        return redirect(url_for('home'))


# User Order History
@app.route('/orderhistory')
def orderHistory():

    # Get all order information
    if session['userRole'] == "admin" or session['userRole'] == "user":

        return render_template('orderManager.html', pageType="user")

    else:

        return redirect(url_for('home'))


# User Order History (Single Order)
@app.route('/orderhistory/<orderNumber>')
def orderHistoryView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if session['userRole'] == "admin" or session['userRole'] == "user":

        return render_template('orderView.html', pageType="user")

    else:

        return redirect(url_for('home'))


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
    return dict(token=userData[0], name=userData[1], role=userData[2])


def authenticate():
    authToken = request.cookies.get("token")
    userName = request.cookies.get("name")

    if authToken != "":

        session['userRole'] = getUserRole(authToken)

    else:

        session['userRole'] = ""

    return [authToken, userName, session['userRole']]


def getUserRole(UID):

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/getUserRole"
    req = requests.post(url, json={
        "id": UID,
    }, headers={"Content-type": "application/json", "Accept": "text/plain"})

    user = req.json()

    if len(user) == 0:
        role = addNewUser(UID)
    else:
        role = user[0]['role']

    return(role)

def addNewUser(UID):

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/addNewUser"
    req = requests.post(url, json={
        "id": UID,
    })

    return req.text

if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
