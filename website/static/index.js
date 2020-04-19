$(function(){
    $('#sendBtn').bind('click', function(){
        var msg = document.getElementById("msg");
        var value = msg.value;
        msg.value = ""
        $.getJSON('/send_message',
            {val:value},
            function(data){
                
            });
    });
});

window.onload = function(){
    var update_loop = setInterval(update, 100);
    update();
}


function update(){
    fetch("/get_messages")
        .then((response) => {
            return response.json();
        }).then((text) => {
            var messages = "";
            for(value of text["messages"]){
                messages = messages + "<br >" + value; 
            }
            document.getElementById("test").innerHTML = messages;
        });
}

function validate(name){
    if(name.length >= 2){
        return true;
    }
    return false;
}

