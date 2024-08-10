"""
This module provides functionality for retrieving and updating server-related information,
such as temperature and battery status. It interfaces with external libraries (WMI and psutil)
to gather relevant data. The collected information can be utilized for monitoring the server's
temperature and power status.
"""

import psutil
import wmi

class ServerStatus:
    def __init__(self):
        self.current_temperature = 0
        self.highest_temperature = 0
        self.battery_percent = 100

    def get_temperature(self):
        try:
            wmi_interface = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            temperature_info = wmi_interface.Sensor()

            for sensor in temperature_info:
                if sensor.SensorType==u"Temperature" and sensor.Name == u"CPU Package":
                    self.current_temperature = sensor.Value
                    self.highest_temperature = sensor.Max
                    return f"{self.current_temperature}°C({self.highest_temperature}°C)"
                
            return f"N/A (Server issue)"
        
        except Exception as e:
            return f"Error occured while getting temperature value {e}"
            
    def get_battery_percentage(self):
        try:
            battery_info = psutil.sensors_battery()

            if battery_info is not None:
                self.battery_percent = battery_info.percent
                return f"{self.battery_percent}%"

            else:
                return f"Feature unavailable in your server"
        
        except Exception as e:
            return f"Error occured while getting battery percentage {e}"