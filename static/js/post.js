$(document).ready(function() {
    let socket = io('http://' + document.domain + ':' + location.port);

    let em_state = false;

    /*socket.on('connect', function() {
        socket.emit('connect', {data: 'connected to the SocketServer...'});
    });*/

    socket.on('response', function(msg, cb) {

        //if json sent back contains update it means data in here should be updated on the web interface
        if ('update' in msg){
            //update em state on client
            if ('em_on' in msg.update){
                em_state = msg.update.em_on
                //fetch the checkbox
                let elm = document.getElementById('em_check')
                //if check box is equal to the current server state then do nothing
                // else fire the checkbox change event
                if (elm.checked === em_state){
                    console.log('received data from server matches local data');
                } else {
                    console.log('received update from server, updating')
                    elm.checked = em_state
                    elm.dispatchEvent(new Event('change'));
                }

                //update the status text to the bool sent back
                if (em_state) {
                    //get status indicator and set text to on
                    document.getElementById("em_status").innerText = "status: on"
                    //get sibling of the check box which is the label and set that text
                    document.getElementById('em_check').nextElementSibling.innerHTML = 'Turn off'
                } else {
                    //get status indicator and set text to on
                    document.getElementById("em_status").innerText = "status: off"
                    //get sibling of the check box which is the label and set that text
                    document.getElementById('em_check').nextElementSibling.innerHTML = 'Turn on'
                }
            }
        }

        if (cb)
            cb();
    });
    /*$('form#emit').submit(function(event) {
        socket.emit('my_event', {data: $('#emit_data').val()});
        return false;
    });*/

    //listener for checkbox, when clicked sends data back to server
    $('input#em_check').click(function (event) {
        let elm = document.getElementById('em_check')
        socket.emit('toggle_em', {data: elm.checked});
    });

    $('form#toggle_em').submit(function(event) {
        em_state = !em_state;
        socket.emit('toggle_em', {data: em_state});

        return false;
    });
});