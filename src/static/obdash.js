var obdash = (function () {
    return {

        // Sets the server time offset from the client device
        setTime: function () {
            $.post('/time', {
                'epoch': new Date().getTime() / 1000,
            });
        },

        refresh: function(delay) {
            if (delay === undefined) {
                delay = 0;
            }
            setTimeout(function() {
                location.reload(true);
            }, delay);
        }
    };
})();
