// Module pattern
//    http://addyosmani.com/resources/essentialjsdesignpatterns/book/#modulepatternjavascript
var obdash = (function () {

    var eventmap = {};
    var socket = null;

    // Register PIDs to get data for from the server.
    var doPoll = function(pids) {
        socket.emit('poll', {
            pids: pids,
        });
    };

    // Trigger the server to send back any queued data.
    var responseTicker = function() {
        socket.emit('tick');
    };

    return {

        // Make a nice beep sound :)
        beep: function() {
            document.getElementById('audio_beep').play();
        },

        // Register a function to call on the receipt of data for a PID
        on: function(mode, pid, func) {
            eventmap[[mode, pid]] = func;
        },

        // Submit a request for some data for some PIDs
        request: function(pids) {
            if (pids === undefined) {
                throw 'start: Array of PIDs is required';
            }

            if (!$.isArray(pids)) {
                throw 'start: First argument (PIDs) must be an array';
            }
            doPoll(pids);
        },

        // Submit the current time to the server to update the internal clock
        setTime: function () {
            $.post('/time', {
                'epoch': new Date().getTime() / 1000,
            });
        },

        // Start the timed processes etc.
        init: function() {
            // Create the socket
            socket = io.connect(
                'http://' + document.domain + ':' + location.port
            );

            // Associate the response handler with the socket
            socket.on('value', function(responseData) {
                if (eventmap.hasOwnProperty(responseData.pid)) {
                    eventmap[responseData.pid]({
                        'timestamp': responseData.timestamp,
                        'value': responseData.value,
                    });
                }
            });

            // Start the response gathering polling from client to server. We
            // only "gather" 10 times a second - this doesn't matter as the
            // data is timestamped at the OBD end to a far higher resolution.
            setInterval(function() {
                responseTicker();
            }, 100);

        },

    };
})();

$(document).ready(function(){
    obdash.setTime();
    obdash.init();
});
