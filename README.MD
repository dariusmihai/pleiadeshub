# Pre-Alpha stage. Not suitable for use just yet.
**But stay close, something goooood is cooking !**  

## Overview

This project provides a simple API that:

- Advertises itself on the network using mDNS as `pleiadeshub.local`.
- Detects and connects to a running PHD2 instance (scanning ports 4000-4010).
- Establishes a websockets connection with a web front-end accessible at http://pleiadeshub.local:5000
- Sends relevand PHD2 events to a web front-end.
- Runs on Linux, Windows, and macOS.
- **Supports WebSockets** for real-time guiding data streaming.
- **Includes a simple web UI** for visualization.

## Requirements

### Clone this repository - choose your favourite method below
HTTPS: 
```sh
git clone https://github.com/dariusmihai/pleiadeshub.git
```   
SSH:
```sh 
git clone git@github.com:dariusmihai/pleiadeshub.git
``` 
GitHub CLI:
```sh
gh repo clone dariusmihai/pleiadeshub
```  

  
### **Python Version**  

- Python 3.8+
- Install dependencies using:
  ```sh
  pip install flask requests zeroconf flask-socketio simple-websocket
  ```
- If this doesn't work, you might need venv. See [Troubleshooting](#error-on-installing-packages-via-pip)



## Running the Server  

#### 1. Run the server:
First, a one-time command: `chmod +x start.sh`, then:
```shell
./start.sh
```
or if you like typing more letters into the terminal each time you start it:
```sh
python pleiadeshub.py
```

#### 2. Open the web UI in a browser
```shell
http://pleiadeshub.local:5000/
```

#### 3. Access API at (NOT IMPLEMENTED YET. ONLY WEBSOCKETS ARE CURRENTLY SUPPORTED):
```shell
curl http://localhost:5000/get-phd2-status
```




## How It Works  
- The service scans for an active PHD2 instance on ports 4000-4010.
- Once found, it polls PHD2's API for guiding error data.
- When PHD2 events are detected, these are immediately sent to the browser via websockets.
- The service announces itself via mDNS (pleiadeshub.local).
- WebSockets allow real-time updates, eliminating the need for polling.
- A simple web UI provides live visualization of guiding errors and general info.  

## Troubleshooting
- If no PHD2 instance is detected, manually specify a port in the code.
- Ensure firewall rules allow traffic on port 5000.

### Error on installing packages via PIP  
#### Problem
× This environment is externally managed
To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.  
#### Solution
1. Install venv if it’s not installed already:
```bash
sudo apt install python3-venv
```
2. Create a virtual environment: In the directory where you want your project, run:
```bash
python3 -m venv venv
```  
3. Activate the Virtual environment:  
    - On Linux/MacOS
        ```bash
        sudo apt install python3-venv
        ```  
    - On Windows  
        ```cmd
        .\venv\Scripts\activate
        ```  

4. Install the dependencies: Now that you are inside the virtual environment, you can install the required packages:  
```bash
pip install flask requests zeroconf flask-socketio simple-websocket
```
5. Run the application
```bash
python pleiadeshub.py
```

## Future Enhancements
- Improve the UI with additional charting options.
- Allow user-configurable PHD2 port selection from the web UI.
- Implement logging for diagnostics and error tracking.