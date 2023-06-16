DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS residents;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_types;


-- TABLES
CREATE TABLE room_types
(
    id SERIAL NOT NULL UNIQUE,
    name VARCHAR(225) NOT NULL
);

CREATE TABLE rooms
(
    id SERIAL NOT NULL UNIQUE,
    name VARCHAR(225) NOT NULL,
    type_id INT REFERENCES room_types(id) ON DELETE CASCADE NOT NULL,
    capacity SMALLINT NOT NULL CHECK (capacity > 0)
);

CREATE TABLE residents
(
    id SERIAL NOT NULL UNIQUE,
    name VARCHAR(225) NOT NULL
);

CREATE TABLE bookings
(
    id SERIAL NOT NULL UNIQUE,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE NOT NULL,
    resident_id INT REFERENCES residents(id) ON DELETE CASCADE NOT NULL,
    start_ TIMESTAMP NOT NULL,
    end_ TIMESTAMP NOT NULL
);


-- DUMMY DATA
INSERT INTO room_types (name) VALUES
  ('Single'),
  ('Double'),
  ('Triple');

INSERT INTO rooms (name, type_id, capacity) VALUES
  ('101', 1, 1),
  ('102', 1, 2),
  ('201', 2, 2),
  ('202', 2, 2),
  ('203', 2, 3);

INSERT INTO residents (name) VALUES
  ('John Smith'),
  ('Jane Doe'),
  ('Bob Johnson');

INSERT INTO bookings (room_id, resident_id, start_, end_) VALUES 
  (1, 1, '2023-06-10 14:00:00', '2023-06-12 12:00:00'),
  (2, 2, '2023-06-15 16:00:00', '2023-06-20 10:00:00'),
  (3, 3, '2023-06-25 12:00:00', '2023-06-28 14:00:00');
