"""
This module manages the communication of server conditions to the client through alerts.
It includes a shutdown feature designed to integrate with the WebSocket for interpreting
the shutdown command. The forceful shutdown is automatically triggered in cases where
critical alerts are sent but the client fails to respond with any action.
"""

import os
from .continous_checkup import ContinousCheckup

class ServerController:
    def __init__(self):
        self.temperature_threshold = 80
        self.battery_percent_threshold = 8
        self.non_response_counter = 0
        self.non_response_threshold = 3
        self.continous_checkup = ContinousCheckup()

    def send_alert(self):
        self.continous_checkup.check_up()

        if self.continous_checkup.server_status.current_temperature >= self.temperature_threshold and \
        self.continous_checkup.server_status.battery_percent <= self.battery_percent_threshold:
            
            self.non_response_counter += 1

            return f"The server is experiencing overheat and the charge is low"

        elif self.continous_checkup.server_status.current_temperature >= self.temperature_threshold:

            self.non_response_counter += 1

            return f"The server is experiencing overheat"

        elif self.continous_checkup.server_status.battery_percent <= self.battery_percent_threshold:

            self.non_response_counter += 1

            return f"The server's charge is low, your server may shut down at any moment"

        return f"No Alert"
        
    def shutdown(self):
        try:
            os.system("shutdown /s /f /t 10")
            return f"The server is shutting down, all connections will be lost"
        
        except OSError as e:
            return f"OS Error occurred while shutting down: {e}, please shutdown the server manually"
        
        except Exception as e:
            return f"Error while trying to shutdown: {e}, please shutdown the server manually"
    
    def forceful_shutdown(self):
        """
        If a client does not respond to critical server alerts which require shutdown,
        then this function will be triggered according to how many critical alerts
        were sent without any response
        """

        if self.non_response_counter == self.non_response_threshold:
            if self.continous_checkup.server_status.current_temperature >= self.temperature_threshold:
                self.shutdown()

                return f"Forceful shutdown triggered due to high temperature"
        
            if self.continous_checkup.server_status.battery_percent == self.battery_percent_threshold:
                self.server_controller.shutdown()

                return f"Forceful shutdown is triggered due to low charge"
        
        return f"Forceful shutdown not triggered" 
    

# Additional functionality needed: If there was no critical alert within 10 minutes and the non_response_counter is > 0 then reset the counter to 0
# Additional functionality needed: Before performing shutdown, check if the file we deal with is saved first