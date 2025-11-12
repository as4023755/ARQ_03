

USE bus_reservation;


INSERT INTO buses (bus_name, bus_type, total_seats)
VALUES
('Express Line 101', 'AC', 40),
('City Rider', 'Non-AC', 50),
('Night Cruiser', 'Sleeper', 30);


INSERT INTO routes (source, destination, distance)
VALUES
('Mumbai', 'Pune', 150),
('Delhi', 'Jaipur', 270),
('Bangalore', 'Chennai', 340);


INSERT INTO schedules (bus_id, route_id, departure_time, arrival_time, fare)
VALUES
(1, 1, '2025-11-09 08:00:00', '2025-11-09 12:00:00', 450.00),
(2, 2, '2025-11-09 09:30:00', '2025-11-09 14:00:00', 600.00),
(3, 3, '2025-11-09 22:00:00', '2025-11-10 05:00:00', 900.00);


SELECT * FROM buses;
SELECT * FROM routes;
SELECT * FROM schedules;
