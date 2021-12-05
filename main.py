import logging
from flask import Flask, render_template, request, session, url_for, redirect
import json
import requests
from datetime import datetime

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

        if (basketData['quantity'] > 0):

            if (session.get('basket') is None):

                session['basket'] = [basketData]

            else:

                updatedBasket = session['basket'].copy()

                alreadyExists = False

                for index, item in enumerate(session['basket']):

                    if (item['productID'] == basketData['productID']):
                        updatedBasket[index]['quantity'] += basketData['quantity']
                        alreadyExists = True

                if (alreadyExists == False):
                    updatedBasket.append(basketData)

                session['basket'] = updatedBasket

        else:

            print("quantity cant be less than one.")

    return render_template('home.html', products=loadProducts())


# User Checkout
@app.route('/checkout')
def checkout():

    if(request.cookies.get("token")):

        if (session.get('basket') is None):

            return redirect(url_for('home'))

        else:

            basket = loadBasketContents()
            
            subTotal = 0
            for item in basket:
                subTotal += (item['product'][0]['price'] * item['quantity'])

            session['subtotal'] = subTotal

            tax = subTotal/4
            session['tax'] = tax

            session['total'] = tax + subTotal

            if(len(basket) == 0):
                disable = True
            else:
                disable = False

            return render_template('checkout.html', basket=basket, subTotal="{:.2f}".format(subTotal), tax="{:.2f}".format(tax), orderTotal = "{:.2f}".format(subTotal+tax), disable=disable)

    else:
        
        return redirect(url_for('home'))

@app.route('/checkout/removeItem', methods=['POST', 'GET'])
def removeItem():
    if(request.method == "POST"):

        removeItemJSON = request.get_json()

        removeItemID = removeItemJSON['productID']

        updatedBasket = []

        for item in session['basket']:
            if item['productID'] != removeItemID:
                updatedBasket.append(item)

        session['basket'] = updatedBasket

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/checkout/address')
def checkoutAddress():
    return render_template('orderAddress.html')

@app.route('/checkout/address/save', methods=['POST', 'GET'])
def saveAddresses():
    if(request.method == "POST"):

        session['address_data'] = (request.form).to_dict()

        address_data = session['address_data']

        basket_data = loadBasketContents()

        # Removes the _id field that mongoDB assigns as it causes an error in the POST request
        for item in basket_data:
            product = item['product'][0]
            del product['_id']

        session['basket_data'] = basket_data

        cost_data = {"subtotal":"{:.2f}".format(session['subtotal']), "tax":"{:.2f}".format(session['tax']), "total":"{:.2f}".format(session['total'])}

        session['cost_data'] = cost_data

        orderID = submitOrder(basket_data, cost_data, address_data)

        clearCheckoutSessions()

        # Cloud function to save order and shit then save order number to session

        return redirect(url_for('orderSubmitted', orderNumber = orderID))

@app.route('/ordersubmitted/<orderNumber>')
def orderSubmitted(orderNumber):

    # Cloud function to use saved order number to pull all the order data


    return render_template('orderSubmitted.html', orderNumber = orderNumber, basket = session['basket_data'], cost = session['cost_data'], address = session['address_data'])

# Admin Order Manager
@app.route('/ordermanager')
def orderManager():

    # Get all order information
    if (session['userRole'] == "admin"):

        orders = loadOrders("All", request.cookies.get("token"))

        return render_template('orderManager.html', pageType="admin", order = orders)

    else:

        return redirect(url_for('home'))


# Admin Order Manager (Single order)
@app.route('/ordermanager/<orderNumber>')
def orderView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if (session['userRole'] == "admin"):

        order = loadOrders("Single", int(orderNumber))

        return render_template('orderView.html', pageType="admin", order = order)

    else:

        return redirect(url_for('home'))

# Admin Order Manager (Single order)
@app.route('/ordermanager/<orderNumber>/update', methods=['POST', 'GET'])
def updateOrder(orderNumber):

    if(request.method == "POST"):

        orderStatus = request.form.get('orderStatus')
        trackingURL = request.form.get('trackingURL')

        url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/updateOrder"
        requests.post(url, json={
            "update_data": {
                "orderID":orderNumber,
                "orderStatus":orderStatus,
                "trackingURL":trackingURL
            },
        }, headers={"Content-type": "application/json", "Accept": "text/plain"})

        return redirect(url_for('orderView', orderNumber = orderNumber))

# User Order History
@app.route('/orderhistory')
def orderHistory():

    # Get all order information
    if (session['userRole'] == "admin" or session['userRole'] == "user"):

        orders = loadOrders("All", request.cookies.get("token"))

        return render_template('orderManager.html', pageType="user", order=orders)

    else:

        return redirect(url_for('home'))


# User Order History (Single Order)
@app.route('/orderhistory/<orderNumber>')
def orderHistoryView(orderNumber):

    # Cloud function to get order details using 'orderNumber'
    if (session['userRole'] == "admin" or session['userRole'] == "user"):

        order = loadOrders("Single", int(orderNumber))

        return render_template('orderView.html', pageType="user", order=order)

    else:

        return redirect(url_for('home'))


# Admin Controls
@app.route('/admin')
def admin():

    return render_template('admin.html', products=loadProducts())

@app.route('/admin/create', methods=['POST', 'GET'])
def createProduct():

    if(request.method == "POST"):

        url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/createProduct"
        requests.post(url, json=
        {
            "product_data":{
                "id":request.form.get('productCodeInput'),
                "name":request.form.get('productNameInput'),
                "desc":request.form.get('ProductDescInput'),
                "productUrl":"",#request.form.get('orderStatus'),
                "price":float(request.form.get('productPriceInput'))
            }  
        }, headers={"Content-type": "application/json", "Accept": "text/plain"})

    return redirect(url_for('admin'))


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
def loadOrders(amount, uid):

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/getOrder"

    req = requests.post(url, json={
        "request_data":{
            "amount":amount,
            "role":session['userRole'],
            "UID":str(uid)
        }
    })
    
    return req.json()


# Loads the information about a single order.
def loadSingleOrder(orderID):

    # TODO Cloud function
    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/"
    req = requests.post(url, json={
        "id": str(orderID),
        })

    return req.json()


def loadBasketContents():

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/getBasketItemsByID"
    req = requests.post(url, json={
        "basket": session['basket'],
        })

    basketItems = req.json()

    return basketItems

def submitOrder(basket_data, cost_data, address_data):

    date = datetime.now()

    url = "https://europe-west2-teak-amphora-328909.cloudfunctions.net/createNewOrder"
    req = requests.post(url, json={
    "order_data":{
        "userID":request.cookies.get("token"),
        "basket_data":basket_data,
        "cost_data":cost_data,
        "address_data":address_data,
        "order_date":date.strftime("%d/%m/%y")
    }
})

    return req.text
    

def clearCheckoutSessions():

        session['basket'] = []
        session['subtotal'] = None
        session['tax'] = None
        session['total'] = None


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
