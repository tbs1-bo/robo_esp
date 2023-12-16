PRAGMA writable_schema = 1;
DELETE FROM sqlite_master WHERE TRUE ;
PRAGMA writable_schema = 0;
VACUUM;
PRAGMA integrity_check;
-- Create direction table
CREATE TABLE direction (
    direction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(255)
);

-- Create robot table
CREATE TABLE robot (
    robot_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(255)
);

-- Create json table
CREATE TABLE json (
    json_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    data TEXT
);

-- Create motor table
CREATE TABLE motor (
    motor_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(255)
);

-- Create command table
CREATE TABLE command (
    command_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tstamp FLOAT,
    robot_id INTEGER,
    json_id INTEGER,
    FOREIGN KEY (robot_id) REFERENCES robot(robot_id),
    FOREIGN KEY (json_id) REFERENCES json(json_id)
);

-- Create motor_command table
CREATE TABLE motor_command (
    motor_command_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    command_id INTEGER,
    motor_id INTEGER,
    direction_id INTEGER,
    speed INT,
    FOREIGN KEY (command_id) REFERENCES command(command_id),
    FOREIGN KEY (motor_id) REFERENCES motor(motor_id),
    FOREIGN KEY (direction_id) REFERENCES direction(direction_id)
);

INSERT INTO direction (name) VALUES ('forward'), ('backward');
INSERT INTO motor (name) VALUES ('left'), ('right');
INSERT INTO robot (name) VALUES ('rob_trottmann');

