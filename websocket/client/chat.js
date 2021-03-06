var ws;
var username;

function onKeyUp(event)
{
    if (event.keyCode == 13)
        sendMessage();
}

function sendMessage()
{
    message = document.getElementById("message");
    if (message.value)
    {
        var f=new Date();
        cad=f.getHours()+":"+f.getMinutes()+":"+f.getSeconds();
        window.status =cad;
        setTimeout("mostrarhora()",1000);
        ws.send("<strong>" + username + "</strong>: " + message.value+cad);
        message.value = "";
    }
    message.focus();
}

function checkSupport()
{
    if (!("WebSocket" in window))
    {
        document.getElementById("login").innerHTML = "Este navegador no soporta WebSockets.";
    }
}

function loadChat()
{
    username = document.getElementById("username").value;
    if (!username)
        return;

    document.getElementById("login").hidden = true;
    document.getElementById("chat").hidden = false;

    messages = document.getElementById("messages");
    messages.innerHTML = "";

    ws = new WebSocket("ws://127.0.0.1:9998");

    ws.onopen = function()
    {
      var f=new Date();
      cad=f.getHours()+":"+f.getMinutes()+":"+f.getSeconds();
      window.status =cad;
      setTimeout("mostrarhora()",1000);
        ws.send(username + " ha ingresado al chat.   "+"       "+cad   );
    };

    ws.onclose = function()
    {
        chat.innerHTML = "Se ha perdido la conexión."
    };

    ws.onmessage = function(evt)
    {
        messages.innerHTML += evt.data + "<br />";
        messages.scrollTop = messages.scrollHeight;
    };
}

function closeChat()
{
    ws.send(username + " se ha desconectado.");
    ws.close();
}
