"""
MIT License

Copyright (c) 2025 Darius Mihai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import threading
from .guider import Guider
import logging
from ..mixins.EventEmitterMixin import EventEmitterMixin

class PHD2Connector(EventEmitterMixin):
    def __init__(self, host:str='localhost'):
        """Constructor to initialize PHD2 connector with optional host and port."""
        super().__init__()
        self.host = host
        self.phd2 = Guider(host)
        self.logger = logging.getLogger(__name__)

        # Register event listener after initialization
        self._lock = threading.Lock()
        self._apply_event_listeners()

    def connect(self) -> None:
        """Attempts to connect to PHD2 with error handling."""
        with self._lock:
            if not self.is_connected():
                try:
                    self.phd2.Connect()
                    self.logger.info("Successfully connected to PHD2.")
                except Exception as e:
                    self.logger.info(f"Failed to connect to PHD2: {e}")
            else:
                self.logger.info("Already connected")

    # @Guider.on(self.phd2, Guider.EVENT_GLOBAL_RECEIVED) - This will not work because the event is on the instance, not on the class
    def _on_phd2_message_received(self, instance_id: int, event_name: str, *args, **kwargs):
        self.logger.info(f"I received a message from instance {instance_id}")
        self.logger.info(f"{event_name}, Args {args}, Kwargs {kwargs}")
        # Assuming the event data is in `args[0]` and it contains a dictionary
        if args and isinstance(args[0], dict):
            event_data = args[0]
            cleaned_data = self._clean_event_data(event_data)
            if event_name == 'StarLost':
                cleaned_data = self._clean_event_data_star_lost(cleaned_data)
            # Emit the event with the cleaned-up data
            self._emit_event(event_name, cleaned_data)
    
    def _on_phd2_connection(self, connected:bool, *args, **kwargs) -> None:
        self.logger.info(f"PHD2 connection state change: {connected}")

    def _apply_event_listeners(self) -> None:
        """
        Method to apply the event listener after the object is fully initialized.
        """
        # Registering the method as an event listener
        self.phd2.on(Guider.EVENT_GLOBAL_RECEIVED)(self._on_phd2_message_received)
        self.phd2.on(Guider.EVENT_CONNECT)(self._on_phd2_connection)

    def disconnect(self) -> None:
        """Attempts to disconnect from PHD2 safely."""
        with self._lock:
            if(self.is_connected()):
                try:
                    self.logger.info("Disconnecting from PHD2...")
                    self.phd2.Disconnect()
                    self.logger.info("Successfully disconnected.")
                except Exception as e:
                    self.logger.info(f"Error disconnecting from PHD2: {e}")
            else:
                self.logger.info("Already disconnnected")

    def getPHD2(self) -> Guider:
        return self.phd2
    
    def is_connected(self) -> bool:
        """Check if PHD2 is currently connected."""
        # Assuming Guider has a method to check connection status
        return self.phd2.conn is not None
    
    def _clean_event_data(self, event_data: dict) -> dict:
        """Remove unnecessary fields from the event data."""
        fields_to_remove = ['Host', 'Inst', 'Frame', 'Time']
        return {key: value for key, value in event_data.items() if key not in fields_to_remove}
    
    def _clean_event_data_star_lost(self, event_data: dict) -> dict:
        fields_to_keep = ['Event', 'Status', 'Timestamp']
        return {key: value for key, value in event_data.items() if key in fields_to_keep}
