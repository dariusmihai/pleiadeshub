import flask
import requests
import socket
import logging
from flask_socketio import SocketIO, emit
import json
import signal
import sys
import debugpy
from src.phd2.PHD2Connector import PHD2Connector
import argparse
from src.MDNS import MDNS

# Set up argument parser
parser = argparse.ArgumentParser(description="With optional debugger")
parser.add_argument('-debug', action='store_true', help='Enable the debugger')

# Parse the arguments
args = parser.parse_args()

# Check if the script is frozen (running from an executable) using sys.frozen
if getattr(sys, 'frozen', False):
    print("Warning: Running in frozen mode. Debugger may not work.")
else:
    if args.debug:
        debugpy.listen(('0.0.0.0', 5678))
        print("Waiting for debugger attach")
        debugpy.wait_for_client()
        print("Debugger ready to attach")

app = flask.Flask(__name__, static_folder='static')  # Serve static files from 'static'
socketio = SocketIO(app)  # For WebSocket support

"""
DEFAULT_PORTS = list(range(4400, 4410))
current_phd2_port = None
phd2_running = False
"""

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

phd2 = PHD2Connector("localhost")

def connect_phd2():
    phd2.connect()

@phd2.on('StarLost')
def _on_phd2_star_lost(data:dict) -> None:
    socketio.emit('phd2_star_lost', data)

@phd2.on('GuideStep')
def _on_phd2_guide_step(data:dict) -> None:
    socketio.emit('phd2_guide_step', data)

# Web UI page for PHD2 status visualization
@app.route('/')
def index():
    connect_phd2()
    return flask.render_template('index.html')  # This will automatically look in the templates/ folder

# WebSocket event handler to handle real-time updates
@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

"""
@app.route('/shutdown')
def shutdown():
    socketio.stop()

@socketio.on('kill')
def kill_socketio():
    socketio.stop()
"""
@app.after_request
def remove_permissions_policy(response):
    if 'Permissions-Policy' in response.headers:
        del response.headers['Permissions-Policy']
    return response

# Graceful shutdown handler
def shutdown(sig, frame):
    print("Shutting down gracefully...")
    if mdns:
        mdns.stop_mdns_service  # Close mDNS service
    sys.exit(0)  # Exit the program

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, shutdown)  # Handle Ctrl+C (SIGINT)
signal.signal(signal.SIGTERM, shutdown)  # Handle termination signal (SIGTERM)

if __name__ == '__main__':
    mdns = MDNS(domain="pleiadeshub", port=5000)
    mdns.start_mdns_service()
    socketio.run(app, host='0.0.0.0', port=5000)
    connect_phd2()
