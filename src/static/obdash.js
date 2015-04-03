var obdash = (function () {

    var pollIntervalTimer = null;
    var eventmap = {};
    var socket = null;

    var setupSocket = function() {
        socket = io.connect(
            'http://' + document.domain + ':' + location.port);
        socket.on('value', function(data) {
            console.log(data);
            if (eventmap.hasOwnProperty(data.pid)) {
                eventmap[data.pid]({
                    'timestamp': data.timestamp,
                    'value': data.value,
                });
            }
        });
    }

    var pollTicker = function(activepids) {
        if (socket === null) {
            setupSocket()
        }
        socket.emit('poll', {
            pids: activepids,
        });
    };

    var responseTicker = function() {
        if (socket === null) {
            setupSocket()
        }
        socket.emit('tick');
    };

    setInterval(function() {
        responseTicker();
    }, 50);

    return {

        beep: function() {
            document.getElementById('audio_beep').play();
        },

        on: function(mode, pid, func) {
            eventmap[[mode, pid]] = func;
        },

        oneshot: function(pids) {
            if (pids === undefined) {
                throw 'start: Array of PIDs is required';
            }

            if (!$.isArray(pids)) {
                throw 'start: First argument (PIDs) must be an array';
            }
            pollTicker(pids);
        },

        polled: function(pids, hz) {
            obdash.stop();

            if (pids === undefined || hz === undefined) {
                throw 'start: Array of PIDs and a polling Hz are required';
            }

            if (!$.isArray(pids)) {
                throw 'start: First argument (PIDs) must be an array';
            }

            if (typeof(hz) !== 'number' || hz <= 0 || hz > 20) {
                throw 'start: Second argument (Hz) must be an number 0 < Hz <= 20';
            }

            // Update the interval and array of active pids, do the first run
            pollIntervalTimer = setInterval(function() {
                pollTicker(pids);
            }, 1000 / hz);
            pollTicker(pids);

        },

        refresh: function(delay) {
            if (delay === undefined) {
                delay = 0;
            }
            setTimeout(function() {
                location.reload(true);
            }, delay);
        },

        // Sets the server time offset from the client device
        setTime: function () {
            $.post('/time', {
                'epoch': new Date().getTime() / 1000,
            });
        },

        stop: function() {
            if (pollIntervalTimer !== null) {
                clearInterval(pollIntervalTimer);
            }
            socket = null;
        },

    };
})();

$(document).ready(function(){
    obdash.setTime();
});
