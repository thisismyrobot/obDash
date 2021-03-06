$(document).ready(function(){
    // States for the app
    var modeEnum = {
        UNSTAGED: 0,
        STAGED: 1,
        TIMING: 2,
        TIMED: 3,
        DONE: 4,
    };
    var mode = modeEnum.UNSTAGED;
    var starttime;
    var duration;
    var kph;

    // Hook up the restart button
    $('#restart_timing').click(function(){
        mode = modeEnum.UNSTAGED;
    });

    // Listen for the kph, step through the modes
    obdash.on(0x01, 0x0D, function(data) {

        kph = data.value;

        if (mode === modeEnum.UNSTAGED)
        {
            // Wait until we have stopped.
            if (kph > 0) {
                return;
            }
            mode = modeEnum.STAGED;
            starttime = null;
        }

        if (mode === modeEnum.STAGED) {
            // If we are moving
            if (kph > 0) {
                // Start timing
                starttime = data.timestamp;
                mode = modeEnum.TIMING;
            }
        }

        if (mode === modeEnum.TIMING) {
            // Detect reaching/crossing 100 kph
            if (kph >= 100)
            {
                duration = data.timestamp - starttime;
                console.log(duration);
                mode = modeEnum.TIMED;
                return;
            }
        }

        if (mode === modeEnum.TIMED) {
            // TODO: Save to log???
            mode = modeEnum.DONE;
        }

    });

    // Start the polling
    setInterval(function() {
        obdash.request([
            [0x01, 0x0D], // KPH
        ]);
    }, 50); // 20 times/second

    // Fire up a UI widget
    setInterval(function() {
        if (mode !== modeEnum.DONE) {
            $('.mode').hide();
        }
        switch(mode) {
            case modeEnum.UNSTAGED:
                $('.mode.unstaged').show();
                break;
            case modeEnum.STAGED:
                $('.mode.staged').show();
                break;
            case modeEnum.TIMING:
                $('.mode.timing').show();
                break;
            case modeEnum.TIMED:
                $('.mode.timed').show();
                $('.mode.timed .duration').text(duration);
                break;
        }
    }, 1000);

});