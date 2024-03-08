CREATE DATABASE IF NOT EXISTS db;

USE db;

CREATE TABLE health_records (
    RecordID INT NOT NULL AUTO_INCREMENT, patientID INT NOT NULL, date DATE NOT NULL, diagnosis VARCHAR(255), treatment VARCHAR(255), medicalcondition VARCHAR(255), familyhistory VARCHAR(255), healthcareprovider VARCHAR(255), PRIMARY KEY (RecordID)
);

INSERT INTO
    health_records (
        patientID, date, diagnosis, treatment, medicalcondition, familyhistory, healthcareprovider
    )
VALUES (
        1, '2023-01-15', 'Hypertension', 'Prescribed medication and lifestyle changes', 'Hypertension', 'None', 'Dr. Smith'
    ),
    (
        2, '2023-02-20', 'Diabetes Type 2', 'Insulin therapy and dietary modifications', 'Diabetes Type 2', 'Family history of diabetes', 'Dr. Johnson'
    );

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, salt VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE, first_name VARCHAR(100), last_name VARCHAR(100)
);

INSERT INTO
    users (
        username, password, salt, email, first_name, last_name
    )
VALUES (
        'john_doe', 'hashed_password1', 'random_salt_1', 'john@example.com', 'John', 'Doe'
    ),
    (
        'emma_smith', 'hashed_password2', 'random_salt_2', 'emma@example.com', 'Emma', 'Smith'
    );