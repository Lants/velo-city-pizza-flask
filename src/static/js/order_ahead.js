const base_url = "localhost:5000";

// STARTUP
var webpage = window.location.href;
console.log("HTML Loaded: " + webpage);
if (webpage.indexOf('order_ahead') !== -1) {
    orderAheadInit();
}
else {
    console.log("Order Ahead Error: Wrong URI");
}

function orderAheadInit() {
    console.log("Page Init: Order Ahead");
    var socket = io.connect(base_url);
}