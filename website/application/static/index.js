const add_messages = async (msg, scroll) => {
    if (typeof msg.name !== "undefined"){
        var date  = dateNow()

        if (typeof msg.time !== "undefined"){
            var n = msg.time;
        }
        else {
            var n = date;
        }

        var global_name = await load_name()

        // personal message is displayed darker and on the left
        var content = "<div class='container'>" + "<b style='color:#000' class='right'>" + msg.name + "</b><p>" + msg.message + "</p>";
        if(global_name === msg.name){
            content = "<div class='container darker'>" + "<b style='color:#000' class='left'>" + msg.name + "</b><p>" + msg.message + "</p><span class='time-left'>" + msg.time + "</span>";
        }

        var messageDiv = document.getElementById("messages");
        messageDiv.innerHTML += content;
    }

    if(scroll) scrollSmoothToBottom("messages");
};


/**
 * fetch request to retrieve the name of the user
 */
const load_name = async () => {
    return await fetch("/get_name")
        .then(async (response) => {
            return await response.json();
        })
        .then((text) => {
            return text["name"];
        });
};


/**
 * fetch request to retrieve the messages posted by the users
 */
const load_messages = async () => {
    return await fetch("/get_messages")
        .then(async (response) => {
            return await response.json();
        })
        .then((text) => {
            return text;
        });
};


/**
 * styling the window to 60% of the height of the browser window (higher than 60% creates a bug when the user is just logged in)
 */
$(function(){
    $(".msgs").css({"height": (($(window).height()) * 0.6) + "px"});

    $(window).bind("resize", () => {
        $(".msgs").css({"height": (($(window).height()) * 0.6) + "px"});
    });
});


/**
 * animation to scroll down through the messages in half a second (500 milliseconds)
 * @param {str} id 
 */
const scrollSmoothToBottom = (id) => {
    var div = document.getElementById(id);
    $("#" + id).animate({
        scrollTop: div.scrollHeight - div.clientHeight
    }, 500);
}


/**
 * returns the current date, hours, and minutes in the format desired
 */
const dateNow = () => {
    var date = new Date();
    var yyyy = date.getFullYear();
    var gg = date.getDate();
    var mm = (date.getMonth() + 1);

    if (gg < 10) gg = "0" + gg;
    if (mm < 10) mm = "0" + mm;

    var current_day = yyyy + "-" + mm + "-" + gg;

    var hours = date.getHours()
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();

    if (hours < 10) hours = "0" + hours;
    if (minutes < 10) minutes = "0" + minutes;
    if (seconds < 10) seconds = "0" + seconds;

    return current_day + " " + hours + ":" + minutes;
};

var socket = io.connect("http://" + document.domain + ":" + location.port);


/**
 * handles user connection and message submission (plus broadcasting the message to all the users logged in)
 */
socket.on("connect", async () => {
    var user_name = await load_name();
    if (user_name != ""){
        socket.emit("event", {
            message: user_name + " just connected to the server!",
            connect: true
        });
    }
    var form = $( "form#msgForm" ).on( "submit", async (e) => {
        e.preventDefault();

        // input from message box
        let msg_input = document.getElementById("msg");
        let user_input = msg_input.value;
        let usr_name = await load_name()

        // clear box value
        msg_input.value = ""

        // send message to other users
        socket.emit( "event", {
            message: user_input,
            name: usr_name
        });
    });
});


// socket.on( "disconnect", async (msg) => {
//     var user_name = await load_name();
//     socket.emit( "event", {
//         message: user_name + " just left the server...",
//     })
// })


/**
 * when "message response" is sent from socket.emit, call add_messages (to update the messages just sent)
 * @param {str} msg 
 */
socket.on("message response", (msg) => {
    add_messages(msg, true);
});


window.onload = async () => {
    var msgs = await load_messages();
    for (i = 0; i < msgs.length; i++){
        scroll = false;
        if (i === msgs.length - 1) scroll = true;
        add_messages(msgs[i], scroll);
    }

    let name = await load_name();
    if (name !== "") $("#login").hide();
    else $("#logout").hide();
};