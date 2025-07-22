import json

import psycopg2
from kafka import KafkaConsumer

from src.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_CONSUMER_GROUP,
    KAFKA_TOPIC,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

if __name__ == "__main__":
    # Create kafka consumer
    print("Connecting to kafka broker...")
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_CONSUMER_GROUP,
            auto_offset_reset="earliest",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        print("Connection to kafka broker successful!")

    except Exception as e:
        print(f"Connection to kafka broker is failed: {e}")
        exit()

    # Create postgres connection
    print("Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
        )
        cur = conn.cursor()
        print("Connection to PostgreSQL database successful")

    except Exception as e:
        print(f"Connection to PostgreSQL database is failed: {e}")
        exit()

    # Consume data until user interupt the script
    try:
        print("Getting data from topic...")
        for message in consumer:
            data = message.value
            try:
                # Look up to device metadata
                cur.execute(
                    f"""
                    SELECT
                        device_name,
                        location,
                        manufacturer
                    FROM bahrul_device_metadata
                    WHERE device_id = '{data['device']}'
                """
                )
                metadata = cur.fetchone()

                # Handle missing data
                if metadata:
                    device_name, location, manufacturer = metadata
                else:
                    device_name = "Unrecognized device"
                    location = "Unknown"
                    manufacturer = "Unknown"

                # Insert to database
                insert_query = """
                        INSERT INTO bahrul_iot_sensor_readings
                        (device_id, device_name, temperature, humidity, timestamp, location, manufacturer)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                record_to_insert = (
                    data["device"],
                    device_name,
                    data["temperature"],
                    data["humidity"],
                    data["timestamp"],
                    location,
                    manufacturer,
                )
                cur.execute(insert_query, record_to_insert)
                conn.commit()
                print(
                    f"Successfuly inserting row: Device {data['device']} read at {data['timestamp']}"
                )

            except Exception as e:
                print(f"Error inserting to database: {e}")
                conn.rollback()

    except KeyboardInterrupt:
        print("Consumer stopped!")

    finally:
        cur.close()
        conn.close()
        consumer.close()
        print("Kafka connection and database connection is closed!")
