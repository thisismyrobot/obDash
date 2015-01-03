// Sets the server time offset from the client device
function setTime() {
    $.post('/time', {
        'epoch': new Date().getTime() / 1000,
    });
}

function refresh(delay) {
    if (delay === undefined) {
        delay = 0;
    }
    setTimeout(function() {
        location.reload(true);
    }, delay);
}
