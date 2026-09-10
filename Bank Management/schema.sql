-- ===================================================
-- Bank Management System Database Schema
-- Database: bank (Mirrors your actual MySQL database)
-- ===================================================

CREATE DATABASE IF NOT EXISTS bank;
USE bank;

-- 1. Customer Table
CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` bigint NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(25) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `account_status` varchar(20) NOT NULL DEFAULT 'active',
  `customer_password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2. Branch Table
CREATE TABLE IF NOT EXISTS `branch` (
  `branch_id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(100) DEFAULT NULL,
  `branch_address` varchar(255) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `ifsc_code` varchar(11) NOT NULL,
  PRIMARY KEY (`branch_id`),
  UNIQUE KEY `ifsc_code` (`ifsc_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3. Accounts Table
CREATE TABLE IF NOT EXISTS `accounts` (
  `account_id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `aacount_number` varchar(20) NOT NULL,
  `balance` decimal(19,4) NOT NULL DEFAULT '0.0000',
  `customer_account_status` varchar(20) NOT NULL DEFAULT 'active',
  `branch_id` int DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `aacount_number` (`aacount_number`),
  KEY `customer_id` (`customer_id`),
  KEY `fk_account_branch` (`branch_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `fk_account_branch` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4. Bank Transaction Table
CREATE TABLE IF NOT EXISTS `bank_transaction` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `account_id` bigint NOT NULL,
  `transaction_type` varchar(20) DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `description_customer` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `bank_transaction_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 5. Loan Table
CREATE TABLE IF NOT EXISTS `loan` (
  `loan_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `loan_type` varchar(50) DEFAULT NULL,
  `loan_amount` decimal(12,2) DEFAULT NULL,
  `interest_rate` decimal(5,2) DEFAULT NULL,
  `loan_date` date DEFAULT NULL,
  `loan_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 6. Fixed Deposit Table (Optional / Extension)
CREATE TABLE IF NOT EXISTS `fixed_deposit` (
  `fd_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `account_id` bigint NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `term_months` int NOT NULL,
  `interest_rate` decimal(5,2) NOT NULL,
  `maturity_amount` decimal(12,2) NOT NULL,
  `start_date` date NOT NULL,
  `maturity_date` date NOT NULL,
  `status` varchar(20) DEFAULT 'Active',
  PRIMARY KEY (`fd_id`),
  KEY `customer_id` (`customer_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `fd_customer_fk` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `fd_account_fk` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 7. Recurring Deposit Table (Optional / Extension)
CREATE TABLE IF NOT EXISTS `recurring_deposit` (
  `rd_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `account_id` bigint NOT NULL,
  `monthly_amount` decimal(12,2) NOT NULL,
  `term_months` int NOT NULL,
  `interest_rate` decimal(5,2) NOT NULL,
  `maturity_amount` decimal(12,2) NOT NULL,
  `total_deposited` decimal(12,2) DEFAULT '0.00',
  `months_paid` int DEFAULT '1',
  `start_date` date NOT NULL,
  `status` varchar(20) DEFAULT 'Active',
  PRIMARY KEY (`rd_id`),
  KEY `customer_id` (`customer_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `rd_customer_fk` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `rd_account_fk` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
