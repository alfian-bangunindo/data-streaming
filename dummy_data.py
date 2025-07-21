import random
from datetime import datetime


class DummyDataIoT:
    def __init__(self, num_devices: int):
        self.num_devices = num_devices
        self.devices = [f"D{i:03}" for i in range(1, self.num_devices + 1)]
        self._initialize_temperature()
        self._initialize_humidity()

    def _initialize_temperature(self):
        self.last_temperature = {d: random.uniform(24, 26) for d in self.devices}

    def _initialize_humidity(self):
        self.last_humidity = {d: random.randint(40, 60) for d in self.devices}

    def generate_data_stream(self):
        device = random.choice(self.devices)
        self.last_temperature[device] += random.gauss(0, 0.025)
        self.last_humidity[device] += int(random.gauss(0, 0.1) * 10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        temperature = round(self.last_temperature[device], 4)
        humidity = round(self.last_humidity[device], 4)
        data = {
            "device": device,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp,
        }

        print(
            f"[{timestamp}] Device {device}: Temperature {temperature}°C, Humidity {humidity}%"
        )

        return data
