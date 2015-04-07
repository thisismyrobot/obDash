function update(data) {
    $.each(data, function(_, item) {
        item[0].refresh(item[1]);
    });
}

$(document).ready(function(){

    var kph = 0;
    var rpm = 0;

    // Listen for the RPM
    obdash.on(0x01, 0x0C, function(data) {
        rpm = data.value;
    });

    // Listen for the KPH
    obdash.on(0x01, 0x0D, function(data) {
        kph = data.value;
    });

    // Set up a polling for the current values
    setInterval(function() {
        obdash.request([
            [0x01, 0x0C],
            [0x01, 0x4D],
        ]);
    }, 200); // 5 times/second

    // Add the actual guages
    var g_rpm = new JustGage({
        id: 'dial_rpm',
        value: 0,
        min: 0,
        max: 6500,
        title: 'RPM',
        label: '',
        valueFontColor: "White",
        gaugeColor: "#333333",
        levelColorsGradient: true,
        refreshAnimationTime: 5000,
        customSectors : [{
            lo: 0,
            hi: 6200,
            color: '#00ff00',
        }, {
            lo: 6201,
            hi: 6500,
            color: '#ff0000',
        }],
    });

    var g_kph = new JustGage({
        id: 'dial_kph',
        value: 0,
        min: 0,
        max: 180,
        title: 'KPH',
        label: '',
        valueFontColor: "White",
        gaugeColor: "#333333",
        customSectors : [{
            lo: 0,
            hi: 130,
            color: '#00ff00',
        }, {
            lo: 131,
            hi: 180,
            color: '#ff0000',
        }],
    });

    // Trigger the updates to the UI
    setInterval(function() {
        update([
            [g_kph, kph],
            [g_rpm, rpm],
        ]);
    }, 100);
});

