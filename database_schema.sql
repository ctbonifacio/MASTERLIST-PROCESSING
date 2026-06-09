-- MC22 FILE Database Schema
-- Database: masterlist_db
-- Host: 172.16.131.242:3307
-- User: usr4mis

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS masterlist_db;
USE masterlist_db;

-- User table for login tracking
CREATE TABLE IF NOT EXISTS `user` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    first_login DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    password_hash VARCHAR(255),
    role VARCHAR(50),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_first_login (first_login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Masterlist data table for processing records
CREATE TABLE IF NOT EXISTS masterlist_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank VARCHAR(50) NOT NULL,
    acc_number VARCHAR(100),
    debtor_name VARCHAR(200),
    status VARCHAR(50) DEFAULT 'Pending',
    claim_paid_amount DECIMAL(15, 2),
    date_import DATE,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bank (bank),
    INDEX idx_status (status),
    INDEX idx_date_import (date_import)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Activity log table
CREATE TABLE IF NOT EXISTS activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(50),
    action VARCHAR(100),
    details TEXT,
    ip_address VARCHAR(45),
    INDEX idx_timestamp (timestamp),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample data for testing
INSERT INTO `user` (username, `name`, first_login, role, status) VALUES
('jvortega', 'Jvortega User', DATE_SUB(NOW(), INTERVAL 3 HOUR), 'Agent', 'ACTIVE'),
('cgmedalla', 'Cyntia G. Medalla', DATE_SUB(NOW(), INTERVAL 5 HOUR), 'Agent', 'ACTIVE'),
('decajes', 'Decajes Agent', DATE_SUB(NOW(), INTERVAL 4 HOUR), 'Agent', 'ACTIVE'),
('ncessopalao', 'Nicolas C. Essopalaos', DATE_SUB(NOW(), INTERVAL 6 HOUR), 'Agent', 'ACTIVE'),
('hpbonabon', 'Herminia P. Bonabon', DATE_SUB(NOW(), INTERVAL 7 HOUR), 'Supervisor', 'ACTIVE')
ON DUPLICATE KEY UPDATE updated_at = NOW();

INSERT INTO masterlist_data (bank, acc_number, debtor_name, status, claim_paid_amount, date_import, details) VALUES
('HSBC UAE', 'ACC001', 'Debtor One', 'Processed', 5000.00, CURDATE(), 'Processed successfully'),
('HSBC UAE', 'ACC002', 'Debtor Two', 'Processed', 3500.00, CURDATE(), 'Processed successfully'),
('HSBC UAE', 'ACC003', 'Debtor Three', 'Pending', 2000.00, CURDATE(), 'Awaiting verification'),
('EIB', 'EIB001', 'Debtor Four', 'Processed', 7500.00, CURDATE(), 'Processed successfully'),
('EIB', 'EIB002', 'Debtor Five', 'Error', 1500.00, CURDATE(), 'Failed validation');

-- Display summary
SELECT 'Users table created' AS status;
SELECT COUNT(*) as total_users FROM `user`;
SELECT 'Masterlist data table created' AS status;
SELECT COUNT(*) as total_records FROM masterlist_data;
