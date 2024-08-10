"""
## Module functionality controversy

- ### New module functionality: 
This module does not check server_status continuously, it is just a coordinator function mainly between
`server_status` and `server_controller`, it is named as `continuous_checkup` because it was originally made
to act that way but the functionality was removed and entangled within the `websocket loop` itself to send
messages periodically.

- ### Old module functionality:
This module is designed to update the status of temperature and battery. It executes periodic check-ups
at specified intervals and notifies the `server_controller` module when updates are available.
"""

from .server_status import ServerStatus

class ContinousCheckup:
    def __init__(self):
        self.server_status = ServerStatus()
    
    def check_up(self):
        self.server_status.get_temperature()
        self.server_status.get_battery_percentage()