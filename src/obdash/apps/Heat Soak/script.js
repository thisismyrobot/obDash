function update(data) {
    $.each(data, function(_, item) {
        item[0].refresh(item[1]);
    });
}

$(document).ready(function(){

    var iat = 0;
    var aat = 0;

    // Listen for the Intake Air Temperature
    obdash.on(0x01, 0x0F, function(data) {
        iat = data.value;
    });

    // Listen for the Ambient Air Temperature
    obdash.on(0x01, 0x46, function(data) {
        aat = data.value;
    });

    // Set up a polling for the current values
    setInterval(function() {
        obdash.request([
            [0x01, 0x0F],
            [0x01, 0x46],
        ]);
    }, 5000); // Every 5 seconds.

    // Add the actual guages
    var g_heatsoak = new JustGage({
        id: 'dial_heatsoak',
        value: 0,
        min: -20,
        max: 20,
        title: 'Heat Soak',
        label: 'Degrees C',
        valueFontColor: "White",
        gaugeColor: "#333333",
        customSectors : [{
            lo: -20,
            hi: 0,
            color: '#00ff00',
        }, {
            lo: 1,
            hi: 5,
            color: '#ffff00',
        }, {
            lo: 6,
            hi: 20,
            color: '#ff0000',
        }],
    });

    var g_iat = new JustGage({
        id: 'dial_iat',
        value: 0,
        min: -20,
        max: 60,
        title: 'Intake Air Temperature',
        label: 'Degrees C',
        valueFontColor: "White",
        gaugeColor: "#333333",
        customSectors : [{
            lo: -20,
            hi: 10,
            color: '#00ff00',
        }, {
            lo: 11,
            hi: 20,
            color: '#ffff00',
        }, {
            lo: 21,
            hi: 60,
            color: '#ff0000',
        }],
    });

    var g_aat = new JustGage({
        id: 'dial_aat',
        value: 0,
        min: -20,
        max: 40,
        title: 'Ambient Air Temperature',
        label: 'Degrees C',
        valueFontColor: "White",
        gaugeColor: "#333333",
        customSectors : [{
            lo: -20,
            hi: 10,
            color: '#00ff00',
        }, {
            lo: 11,
            hi: 15,
            color: '#ffff00',
        }, {
            lo: 16,
            hi: 40,
            color: '#ff0000',
        }],
    });

    // Trigger the updates to the UI
    setInterval(function() {
        iat = 36;
        aat = 21;
        update([
            [g_heatsoak, iat - aat],
            [g_iat, iat],
            [g_aat, aat],
        ]);
    }, 5000);
});

