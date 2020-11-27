$(document).ready(function() {
    //namespace = '/controls';
    var socket = io('http://' + document.domain + ':' + location.port);

    var em_state = false;

    /*socket.on('connect', function() {
        socket.emit('connect', {data: 'connected to the SocketServer...'});
    });*/

    socket.on('response', function(msg, cb) {

        //if json sent back contains update it means data in here should be updated on the web interface
        if ('update' in msg){
            //update em state on client
            if ('em_on' in msg.update){
                em_state = msg.update.em_on
                if (em_state) {
                    document.getElementById('toggle_em').innerHTML = '<input type="submit" value="Toggle Electromagnet (on)">'
                } else {
                    document.getElementById('toggle_em').innerHTML = '<input type="submit" value="Toggle Electromagnet (off)">'
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

    $('form#toggle_em').submit(function(event) {
        em_state = !em_state;
        socket.emit('toggle_em', {data: em_state});

        return false;
    });
});