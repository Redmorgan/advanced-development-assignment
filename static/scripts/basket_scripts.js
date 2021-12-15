/** 
 * @summary Adds the selected item and quantity to the session basket.
 * 
 * @param {string} id - The ID of the product that is getting added to the basket.
*/
function addToCart(id) {
    $.ajax({
        type: "POST",
        url: "store",
        data: JSON.stringify({
            "productID": id,
            "quantity": document.getElementById(`quantityInput_${id}`).value
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
        }
    });
}

/** 
 * @summary Removes the selected item from the session basket.
 * 
 * @param {string} id - The ID of the product that is getting removed from the basket.
*/
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
