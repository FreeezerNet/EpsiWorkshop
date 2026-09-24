CREATE TABLE measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    production_watts INT,
    consumption_watts INT,
    battery_percent FLOAT,
    storage_ratio FLOAT,
    qmode VARCHAR(20)
);

CREATE TABLE sector_allocations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    measurement_id INT,
    sector_name VARCHAR(50),
    required_watts INT,
    allocated_watts INT,
    allocation_percent FLOAT,

    FOREIGN KEY (measurement_id)
        REFERENCES measurements(id)
);

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    event_type VARCHAR(50),
    description TEXT
);