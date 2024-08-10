"""
This module is a service that intergrates `websocket_runner` with `status_controller` which provides
- Temperature
- Battery Percent Remaining
- Alerts

It also has the functionality to process the inputs and save them within data directory
"""

import asyncio
import json

from websockets import ConnectionClosedOK
from datetime import datetime

from server.server_status import ServerStatus
from server.server_controller import ServerController
from location_processing.location import location_provider
from file_input_output.file_input import write_file
from file_input_output.check_file_size import has_file_size_changed

class WebsocketServerService:
    def __init__(self):
        self.server_status = ServerStatus()
        self.server_controller = ServerController()
        self.stop_event = asyncio.Event()
        # self.file_input_output = check_file_size()

    async def websocket_sender_service(self, websocket):
        while not self.stop_event.is_set():
            temperature = self.server_status.get_temperature()
            battery = self.server_status.get_battery_percentage()
            alert = self.server_controller.send_alert()

            message = await websocket.recv()

            deserialized_message = json.loads(message)

            try:
                if deserialized_message["Type"] == "Status":
                    server_status_info = {"Type": "status", "Temperature": temperature, "BatteryPercentage": battery, "alert": alert}

                    serialized_info = json.dumps(server_status_info)
                    print(serialized_info)

                    await websocket.send(serialized_info)

                elif deserialized_message["Type"] == "Shutdown":
                    await self.server_controller.shutdown()
                    
                elif deserialized_message["Type"] == "" or deserialized_message["Type"] == "ping":
                    pass

                elif deserialized_message["Type"] == "Location":
                    deserialized_information = json.loads(message)
                    print(deserialized_information)

                    fileName = deserialized_information["FileName"]
                    latitude = deserialized_information["Latitude"]
                    longitude = deserialized_information["Longitude"]

                    current_time = datetime.now()

                    coordinates =  {
                        "latitude": latitude,
                        "longitude": longitude,
                        "time": current_time.strftime("%H:%M:%S")
                            }

                    coordinates_json = json.dumps(coordinates, indent=4)

                    await write_file(fileName, coordinates_json)

                    # file_changed = has_file_size_changed(fileName)

                    # await file_changed

                    
                    processed_location_data =  {
                        "Latitude": str(latitude),
                        "Longitude": str(longitude),
                        "Time": current_time.strftime("%H:%M:%S")
                        }
                    
                    # else:
                    #     processed_location_data =  {
                    #         "Type": "location",
                    #         "Latitude": 0.000,
                    #         "Longitude": 0.000,
                    #         "Time": current_time.strftime("%H:%M:%S")
                    #             }

                    processed_location_data_json = json.dumps(processed_location_data)

                    print(processed_location_data_json)
                        
                    await websocket.send(processed_location_data_json)

            except ConnectionClosedOK:
                print("\033[1;32mClient closed the connection\033[0m")
                break