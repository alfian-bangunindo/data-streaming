import json
import random
import time

from kafka import KafkaProducer

from src.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, NUM_DEVICES
from src.dummy_data.dummy_data_iot import DummyDataIoT

if __name__ == "__main__":
    # Create kafka producer
    print("Connecting to kafka broker...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
        print("Connection to kafka broker successful!")

    except Exception as e:
        print(f"Connection to kafka broker is failed: {e}")
        exit()

    # Generate dummy data generator from dummy_data module
    dummy_data_generator = DummyDataIoT(num_devices=NUM_DEVICES)
    try:
        print("Get data streaming...")
        while True:
            # Stream data with lag 1 to 2 seconds
            data = dummy_data_generator.next_data_stream()
            producer.send(KAFKA_TOPIC, data)
            time.sleep(random.uniform(1, 2))

    except KeyboardInterrupt:
        print("Data streaming is done!")

    finally:
        producer.flush()
        producer.close()
        print("Kafka connection is closed!")
