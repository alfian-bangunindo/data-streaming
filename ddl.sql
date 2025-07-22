CREATE TABLE bahrul_iot_sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id CHAR(4),
    device_name VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    timestamp TIMESTAMP,
    LOCATION VARCHAR(50),
    manufacturer VARCHAR(50),
    ingestion_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE bahrul_device_metadata (
    device_id CHAR(4) PRIMARY KEY,
    device_name VARCHAR(50),
    LOCATION VARCHAR(50),
    manufacturer VARCHAR(50)
);

INSERT INTO
    bahrul_device_metadata
VALUES
    ('D001', 'Mi Temperature 1', 'Kitchen', 'Xiaomi'),
    (
        'D002',
        'Mi Temperature 2',
        'Living Room',
        'Xiaomi'
    ),
    (
        'D003',
        'Samsung Galaxy Temperature',
        'Gaming Room',
        'Samsung'
    ),
    ('D004', 'Apple Temperature', 'Bedroom', 'Apple'),
    ('D005', 'PX-100D', 'Garage', 'Panasonic');
