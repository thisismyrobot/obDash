// Sets the server time offset from the client device
function setTime() {
    $.post('/time', {
        'epoch': new Date().getTime() / 1000,
    });
}