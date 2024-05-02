from locust import User, task, between
from azure.iot.device import IoTHubDeviceClient, Message
import os
import logging

# Default connection string if environment variable is not set
DEFAULT_CONNECTION_STRING = "HostName=your-iot-hub-name.azure-devices.net;DeviceId=your-device-id;SharedAccessKey=your-shared-access-key"

CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING", DEFAULT_CONNECTION_STRING)
MESSAGE_PAYLOAD = os.getenv("MESSAGE_PAYLOAD", "Hello, Azure IoT Hub!")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IoTUser(User):
    wait_time = between(1, 3)  # Adjust as needed
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        self.client.connect()
    
    def __del__(self):
        self.client.disconnect()

    @task
    def publish_task(self):
        try:
            message = Message(MESSAGE_PAYLOAD)
            self.client.send_message(message)
            logger.info("Message published successfully")
        except Exception as e:
            logger.error("Error publishing message: %s", e)

if __name__ == "__main__":
    user = IoTUser()
    user.publish_task()
