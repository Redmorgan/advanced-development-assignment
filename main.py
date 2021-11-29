import logging
from flask import Flask, render_template, request, session, url_for, redirect
import json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '6ccdb527e50c20c5deb736d0d090f584'


@app.route('/', methods=['POST', 'GET'])
@app.route('/store', methods=['POST', 'GET'])
def home():

    #Clears session if not logged in.
    if (not request.cookies.get("token")):
        session.clear()

    if (request.method == "POST"):

        basketData = request.get_json()

        basketData['quantity'] = int(basketData['quantity'])

        if (session.get('basket') is None):

            session['basket'] = [basketData]

        else:

            currentBasket = session['basket'].copy()
            updatedBasket = session['basket'].copy()

            alreadyExists = False

            for index, item in enumerate(currentBasket):

                if (item['productID'] == basketData['productID']):
                    updatedBasket[index]['quantity'] += basketData['quantity']
                    alreadyExists = True

            if (alreadyExists == False):
                updatedBasket.append(basketData)

            session['basket'] = updatedBasket

    return render_template('home.html', products=loadProducts())


# User Checkout
@app.route('/checkout')
def checkout():

    if(request.cookies.get("token")):

        if (session['basket'] is None):

            return render_template('checkout.html', basket=[])

        else:

            return render_template('checkout.html', basket=loadBasketContents())

    else:
        
        return redirect(url_for('home'))


# Admin Order Manager
@app.route('/ordermanager')
def orderManager():

    # Get all order information
    if (session['userRole'] == "admin"):

        orders = loadOrders()

        return render_template('orderManager.html', pageType="admin", orders = orders)

    else:

        return redirect(url_for('home'))


# Admin Order Manager (Single order)
@app.route('/ordermanager/<orderNumber>')
def orderView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if (session['userRole'] == "admin"):

        return render_template('orderView.html', pageType="admin")

    else:

        return redirect(url_for('home'))


# User Order History
@app.route('/orderhistory')
def orderHistory():

    # Get all order information
    if (session['userRole'] == "admin" or session['userRole'] == "user"):

        orders = loadOrders()

        return render_template('orderManager.html', pageType="user", orders=orders)

    else:

        return redirect(url_for('home'))


# User Order History (Single Order)
@app.route('/orderhistory/<orderNumber>')
def orderHistoryView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if (session['userRole'] == "admin" or session['userRole'] == "user"):

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

    if (authToken != ""):

        session['userRole'] = getUserRole(authToken)

    else:

        session['userRole'] = ""

    return [authToken, userName, session['userRole']]


# Collects a users role based off their ID, if they dont have a role, one is assigned to them.
def getUserRole(UID):

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/getUserRole"
    req = requests.post(url, json={
        "id": UID,
    }, headers={"Content-type": "application/json", "Accept": "text/plain"})

    user = req.json()

    if (len(user) == 0):
        role = addNewUser(UID)

    else:
        role = user[0]['role']

    return(role)


# Creates a new record on mongoDB for the newly registered user.
def addNewUser(UID):

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/addNewUser"
    req = requests.post(url, json={
        "id": UID,
    })

    return req.text


# Loads all products stored on mongoDB
def loadProducts():

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/collectProducts"
    req = requests.get(url, headers={"Content-type": "application/json", "Accept": "text/plain"})

    return req.json()


# Loads all of the order data based on the user role:
#   userRole = Admin or Staff, Loads all orders on the system.
#   userRole = user, Loads all the orders that user has made.
def loadOrders():

    # TODO Cloud function
    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/"

    if (session['userRole'] == "admin" or session['userRole'] == "staff"):
        req = requests.post(url, json={
        "role": "admin",
        })

    elif (session['userRole'] == "user"):
        req = requests.post(url, json={
        "role": "user",
        })

    return req.json()


# Loads the information about a single order.
def loadSingleOrder(orderID):

    # TODO Cloud function
    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/"
    req = requests.post(url, json={
        "id": orderID,
        })

    return req.json()


def loadBasketContents():

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/getBasketItemsByID"
    req = requests.post(url, json={
        "basket": session['basket'],
        })

    basketItems = req.json()

    return basketItems


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
