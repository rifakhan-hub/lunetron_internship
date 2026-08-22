CREATE DATABASE school;     -- create database
USE school;

CREATE TABLE students (         -- defining schema
    id INT PRIMARY KEY,
    names VARCHAR(50),
    age INT,
    course VARCHAR(50)
);

USE school;
SHOW TABLES;            -- show tables in current database

DESCRIBE students;          -- show schema or structure of the students table

-- inserting student record or entries
INSERT INTO students(id, names, age, course)
VALUES 
(1, "Aman", 21, "CSE"),
(2, "Bhumi", 22, "AIML"),
(3, "Dev", 22, "CSE"),
(4, "Garv", 20, "Cyber"),
(5, "harshit", 21, "AIML");

SELECT * FROM students;     -- display all from table

SELECT names, course FROM students;         -- to display particular rows

SELECT * FROM students WHERE id > 2;        -- display column with conditions
SELECT names FROM students WHERE course = 'CSE';

UPDATE students
SET age = 20 
WHERE names = 'Dev';

DELETE FROM students WHERE id = 5;

-- adding a column
ALTER TABLE students
ADD email VARCHAR(50);

-- to update single value
UPDATE students
SET email = "abc@ex.com"
WHERE id = 1;

-- to update multiple value in same column
UPDATE students
SET email = CASE id
    WHEN 2 THEN "pqr@ex.com"
    WHEN 3 THEN "xyz@ex.com"
END
WHERE id IN (2,3);   -- due to workbench safe mode need to put where condtion

ALTER TABLE students
RENAME COLUMN course TO subject;

DESCRIBE students;


