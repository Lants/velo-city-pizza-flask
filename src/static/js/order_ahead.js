const base_url = "localhost:5000";
const DEBUG_MODE = true;

// STARTUP
var webpage = window.location.href;
console.log("HTML Loaded: " + webpage);
if (webpage.indexOf('order_ahead') !== -1) {
    orderAheadInit();
}
else {
    console.log("Order Ahead Error: Wrong URI");
}


// --------------- MAIN FUNCTION (runs on page load) --------------------
function orderAheadInit() {
    console.log("Page Init: Order Ahead");
    // var socket = io.connect(base_url);

    // socket.on('connect', function() {
    //     socket.emit("order-ahead-ready")
    // });



    attachListeners();
}

// Create all listeners. Must be called at END of init function
function attachListeners() {
    // ------------- Button Listeners -------------------
    let category_buttons = document.getElementsByTagName("button");

    for (let i = 0; i < category_buttons.length; i++) {
        const button = category_buttons[i];
        if (DEBUG_MODE) console.log(`buttons = ${button.textContent}`);
        // element.addEventListener("click", categoryButtonOnClick(button.TODO ADD SELECTOR HERE))
    }

    // -------------- Scroll Listener: Sidebar -------------------
        // timeout feature from https://stackoverflow.com/questions/4620906/how-do-i-know-when-ive-stopped-scrolling
        // opacity transition from https://stackoverflow.com/questions/40453881/change-of-opacity-using-css-transition-and-vanilla-javascript-works-only-when-fa
    let sidebar = document.getElementById("order-categories");
    console.log(`sidebar: ${sidebar.id}`);
    let timer = null;
    sidebar.addEventListener("scroll", function() {
        if (timer !== null) clearTimeout(timer);
        timer = setTimeout(function() {
            let chevron = document.getElementById("chevron-down");
            if (detectScrolledToBottom(sidebar)) {
                chevron.style.opacity = 0;
            }
            else {
                chevron.style.opacity = 1;
            }
        }, 7);
    });
}

// ------------------------------- LISTENER HANDLERS ------------------------------------
// Check if given element is scrolled to bottom
    // https://stackoverflow.com/questions/876115/how-can-i-determine-if-a-div-is-scrolled-to-the-bottom
function detectScrolledToBottom(scrollable) {
    return (scrollable.scrollHeight - scrollable.scrollTop - scrollable.clientHeight) < 1;
}