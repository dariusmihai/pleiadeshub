// Connecting to the WebSocket server
var socket = io.connect('http://' + window.location.hostname + ':' + location.port);

// Handle the real-time guiding data and PHD2 status
socket.on('guiding_data', function(data) {
    // Update the guiding errors
    document.getElementById("ra_error").textContent = data.ra_error || "N/A";
    document.getElementById("dec_error").textContent = data.dec_error || "N/A";

    // Update the PHD2 status
    if (data.phd2_running) {
        document.getElementById("phd2-status-text").textContent = "Running";
        document.getElementById("phd2-status-text").style.color = "green";
    } else {
        document.getElementById("phd2-status-text").textContent = "Not Running";
        document.getElementById("phd2-status-text").style.color = "red";
    }
});

socket.on('phd2_star_lost', function(data) {
    console.log('PHD2: Star Lost', data);
});

socket.on('phd2_guide_step', function(data) {
    console.log('PHD2: Guide Step', data);
});