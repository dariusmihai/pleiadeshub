## Overview

This project provides a simple HTTP REST API that:

- Detects and connects to a running PHD2 instance (scanning ports 4000-4010).
- Exposes a `/get-phd2-status` endpoint to fetch real-time guiding errors.
- Advertises itself on the network using mDNS as `pleiadeshub.local`.
- Runs on Linux, Windows, and macOS.
- **Supports WebSockets** for real-time guiding data streaming.
- **Includes a simple web UI** for visualization.

## Requirements

### **Python Version**

- Python 3.8+
- Install dependencies using:
  ```sh
  pip install flask requests zeroconf flask-socketio simple-websocket
  ```

## Running the Server  

#### 1. Run the server:
```shell
python pleiadeshub.py
```

#### 2. Access API at:
```shell
curl http://localhost:5000/get-phd2-status
```

#### 3. Open the web UI in a browser
```shell
http://pleiadeshub.local:5000/
```


## How It Works  
- The service scans for an active PHD2 instance on ports 4000-4010.
- Once found, it polls PHD2's API for guiding error data.
- The REST endpoint provides JSON output with:
```json
{
  "ra_error": 0.12,
  "dec_error": -0.05
}
```
- The service announces itself via mDNS (pleiadeshub.local).
- WebSockets allow real-time updates, eliminating the need for polling.
- A simple web UI provides live visualization of guiding errors.  

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