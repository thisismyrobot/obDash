var obdash = (function () {

    var intervalTimer = null;
    var eventmap = {};
    var socket = null;

    var pollTicker = function(activepids) {
        if (socket === null) {
            socket = io.connect(
                'http://' + document.domain + ':' + location.port);
        }
        socket.emit('poll', {
            pids: activepids,
        });
    };

    return {

        on: function(mode, pid, func) {
            eventmap[[mode, pid]] = func;
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

        start: function(pids, hz) {
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
            intervalTimer = setInterval(function() {
                pollTicker(pids);
            }, 1000 / hz);
            pollTicker(pids);
        },

        stop: function() {
            if (intervalTimer !== null) {
                clearInterval(intervalTimer);
            }
            socket = null;
        },

    };
})();
