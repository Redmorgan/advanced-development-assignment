function addToCart(id) {
    $.ajax({
        type: "POST",
        url: "store",
        data: JSON.stringify({
                "productID": id,
                "quantity":document.getElementById(`quantityInput_${id}`).value
            }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            //alert(JSON.stringify(data));
        }
    });
}

function removeFromCart(id) {
    $.ajax({
        type: "POST",
        url: "checkout/removeItem",
        data: JSON.stringify({
                "productID": id
            }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            location.reload()
        }
    });
}

function saveAddresses() {
    $.ajax({
        type: "POST",
        url: "checkout/address/save",
        data: JSON.stringify({
            "delivery":{
                "firstName":"",
                "lastName":"",
                "ad1":"",
                "ad2":"",
                "city":"",
                "postcode":"",
                "mobile":""
            },
            "billing":{
                "firstName":"",
                "lastName":"",
                "ad1":"",
                "ad2":"",
                "city":"",
                "postcode":"",
                "mobile":""
            }
    }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            location.href('/checkout/confirm')
        }
    });
}
