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
