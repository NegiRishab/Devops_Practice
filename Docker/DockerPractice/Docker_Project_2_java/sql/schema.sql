-- Run this in MySQL before starting the app (optional; JPA can create the table too)
CREATE DATABASE IF NOT EXISTS superhero_db;
USE superhero_db;

CREATE TABLE IF NOT EXISTS superheroes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    power VARCHAR(255) NOT NULL
);
