import random
from datetime import datetime


class DummyDataIoT:
    """
    This class generate fake streaming data of temperature sensor from fake device
    """

    def __init__(self, num_devices: int):
        """
        Initialize devices with name of D001, D002, etc based on `num_devices` input.
        It will also randomly initialize temperature and humidity.

        example:
            num_devices = 2 will generate list of devices = ["D001", "D002"] and Initialize
            last_temperature and last_humidity attribute in the form of dict.
        """
        self.num_devices = num_devices
        self.devices = [f"D{i:03}" for i in range(1, self.num_devices + 1)]
        self._initialize_temperature()
        self._initialize_humidity()

    def _initialize_temperature(self):
        """
        Initialize last temperature read by each devices based on
        uniform distribution with range of 24 to 26 Celcius.
        """
        self.last_temperature = {d: random.uniform(24, 26) for d in self.devices}

    def _initialize_humidity(self):
        """
        Initialize last humidity read by each devices based on
        integer uniform distribution with range of 40 to 60%.
        """
        self.last_humidity = {d: random.randint(40, 60) for d in self.devices}

    def next_data_stream(self) -> dict:
        """
        Randomly select the devices and modify both last_temperature and last_humidity
        by adding some noise to previous value. This method will replace the previous
        value of both attribute with the new one.

        return:
            data: a dictionary that consist of device, temperature, humidity, and timestamp.
        """
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
