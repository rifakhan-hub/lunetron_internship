USE school;

CREATE TABLE courses(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    duration INT,
    fee INT
);

INSERT INTO courses (name, duration, fee)
VALUES
('AIML', 6, 120000),
('CSE', 6, 110000),
('ECE', 4, 100000),
('Cyber', 4, 100000);

select * FROM courses;

