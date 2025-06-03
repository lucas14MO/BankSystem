-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 03, 2025 at 03:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `banksystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `ID_ACCOUNT` int(11) NOT NULL,
  `ID_BANK` int(11) NOT NULL,
  `ID_NATIONALITY` int(11) NOT NULL,
  `NUMBER_ACCOUNT` int(11) DEFAULT NULL,
  `CI_ACCOUNT` int(11) DEFAULT NULL,
  `NAME_ACCOUNT` char(50) DEFAULT NULL,
  `LASTNAME_ACCOUNT` char(50) DEFAULT NULL,
  `PHONE_ACCOUNT` bigint(20) DEFAULT NULL,
  `ADDRESS_ACCOUNT` char(100) DEFAULT NULL,
  `BALANCE_ACCOUNT` decimal(13,2) DEFAULT 0.00,
  `FAULTS_ACCOUNT` smallint(6) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`ID_ACCOUNT`, `ID_BANK`, `ID_NATIONALITY`, `NUMBER_ACCOUNT`, `CI_ACCOUNT`, `NAME_ACCOUNT`, `LASTNAME_ACCOUNT`, `PHONE_ACCOUNT`, `ADDRESS_ACCOUNT`, `BALANCE_ACCOUNT`, `FAULTS_ACCOUNT`) VALUES
(1, 1, 1, 123, 5542041, 'Lucas De Jesus', 'Benitez Miranda', 5950995360867, 'Santa Maria Sector 3', 12000.00, 0),
(3, 1, 1, 5434, 5534212, 'Juan Luis', 'Fritz Morinigo', 59509975234543, 'Asuncion Centro', 5000000.00, 0);

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `ID_BANK` int(11) NOT NULL,
  `NAME_BANK` char(60) DEFAULT NULL,
  `PHONE_BANK` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`ID_BANK`, `NAME_BANK`, `PHONE_BANK`) VALUES
(1, 'Banco Familiar S.A.E.C.A.', '5950111222333'),
(2, 'Banco Atlas S.A.', '5950111222333'),
(3, 'Ueno Bank S.A.E.C.A.', '5950111222333'),
(4, 'Banco Basal S.A.', '5950999888777');

-- --------------------------------------------------------

--
-- Table structure for table `cheque`
--

CREATE TABLE `cheque` (
  `ID_CHEQUE` int(11) NOT NULL,
  `IDEMITTER_ACCOUNT` int(11) NOT NULL,
  `IDRECEPTOR_ACCOUNT` int(11) DEFAULT NULL,
  `ID_CHEQUESTATE` int(11) NOT NULL,
  `PAYMENT_CHEQUE` decimal(13,2) DEFAULT NULL,
  `PUSHDATE_CHEQUE` date DEFAULT NULL,
  `ENDDATE_CHEQUE` date DEFAULT NULL,
  `ADDRESS_CHEQUE` varchar(100) DEFAULT NULL,
  `ISDEFERRED_CHEQUE` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cheque`
--

INSERT INTO `cheque` (`ID_CHEQUE`, `IDEMITTER_ACCOUNT`, `IDRECEPTOR_ACCOUNT`, `ID_CHEQUESTATE`, `PAYMENT_CHEQUE`, `PUSHDATE_CHEQUE`, `ENDDATE_CHEQUE`, `ADDRESS_CHEQUE`, `ISDEFERRED_CHEQUE`) VALUES
(1, 3, 1, 1, 2000000.00, '2025-06-01', '2025-06-30', 'Asuncion Centro', 1);

-- --------------------------------------------------------

--
-- Table structure for table `chequestate`
--

CREATE TABLE `chequestate` (
  `ID_CHEQUESTATE` int(11) NOT NULL,
  `STATE_CHEQUE` char(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chequestate`
--

INSERT INTO `chequestate` (`ID_CHEQUESTATE`, `STATE_CHEQUE`) VALUES
(1, 'Vigente'),
(2, 'Rechazado'),
(3, 'Vencido'),
(4, 'Cobrado');

-- --------------------------------------------------------

--
-- Table structure for table `nationality`
--

CREATE TABLE `nationality` (
  `ID_NATIONALITY` int(11) NOT NULL,
  `COUNTRY_NATIONALITY` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nationality`
--

INSERT INTO `nationality` (`ID_NATIONALITY`, `COUNTRY_NATIONALITY`) VALUES
(1, 'Paraguay'),
(2, 'Argentina'),
(3, 'Brazil'),
(4, 'Uruguay'),
(5, 'Chile'),
(6, 'Bolivia'),
(7, 'Ecuador'),
(8, 'Peru'),
(9, 'Venezuela'),
(10, 'Colombia');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `ID_TRANSACTION` int(11) NOT NULL,
  `ID_BANK` int(11) NOT NULL,
  `IDEMITTER_ACOUNT` int(11) NOT NULL,
  `IDRECEPTOR_ACOUNT` int(11) NOT NULL,
  `AMOUNT_TRANSACTION` decimal(13,2) DEFAULT NULL,
  `DATE_TRANSACTION` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`ID_ACCOUNT`),
  ADD KEY `FK_ACCOUNT_RELATIONS_BANK` (`ID_BANK`),
  ADD KEY `FK_ACCOUNT_RELATIONS_NATIONAL` (`ID_NATIONALITY`);

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`ID_BANK`);

--
-- Indexes for table `cheque`
--
ALTER TABLE `cheque`
  ADD PRIMARY KEY (`ID_CHEQUE`),
  ADD KEY `FK_CHEQUE_ACOUNTCHE_ACCOUNT` (`IDRECEPTOR_ACCOUNT`),
  ADD KEY `FK_CHEQUE_CUENTA_CH_ACCOUNT` (`IDEMITTER_ACCOUNT`),
  ADD KEY `FK_CHEQUE_RELATIONS_CHEQUESTA` (`ID_CHEQUESTATE`);

--
-- Indexes for table `chequestate`
--
ALTER TABLE `chequestate`
  ADD PRIMARY KEY (`ID_CHEQUESTATE`);

--
-- Indexes for table `nationality`
--
ALTER TABLE `nationality`
  ADD PRIMARY KEY (`ID_NATIONALITY`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`ID_TRANSACTION`),
  ADD KEY `FK_TRANSACT_ACOUNTTRA_ACCOUNT` (`IDRECEPTOR_ACOUNT`),
  ADD KEY `FK_TRANSACT_CUENTATRA_ACCOUNT` (`IDEMITTER_ACOUNT`),
  ADD KEY `FK_TRANSACT_RELATIONS_BANK` (`ID_BANK`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `ID_ACCOUNT` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `bank`
--
ALTER TABLE `bank`
  MODIFY `ID_BANK` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `cheque`
--
ALTER TABLE `cheque`
  MODIFY `ID_CHEQUE` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chequestate`
--
ALTER TABLE `chequestate`
  MODIFY `ID_CHEQUESTATE` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `nationality`
--
ALTER TABLE `nationality`
  MODIFY `ID_NATIONALITY` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `ID_TRANSACTION` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account`
--
ALTER TABLE `account`
  ADD CONSTRAINT `FK_ACCOUNT_RELATIONS_BANK` FOREIGN KEY (`ID_BANK`) REFERENCES `bank` (`ID_BANK`),
  ADD CONSTRAINT `FK_ACCOUNT_RELATIONS_NATIONAL` FOREIGN KEY (`ID_NATIONALITY`) REFERENCES `nationality` (`ID_NATIONALITY`);

--
-- Constraints for table `cheque`
--
ALTER TABLE `cheque`
  ADD CONSTRAINT `FK_CHEQUE_ACOUNTCHE_ACCOUNT` FOREIGN KEY (`IDRECEPTOR_ACCOUNT`) REFERENCES `account` (`ID_ACCOUNT`),
  ADD CONSTRAINT `FK_CHEQUE_CUENTA_CH_ACCOUNT` FOREIGN KEY (`IDEMITTER_ACCOUNT`) REFERENCES `account` (`ID_ACCOUNT`),
  ADD CONSTRAINT `FK_CHEQUE_RELATIONS_CHEQUESTA` FOREIGN KEY (`ID_CHEQUESTATE`) REFERENCES `chequestate` (`ID_CHEQUESTATE`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `FK_TRANSACT_ACOUNTTRA_ACCOUNT` FOREIGN KEY (`IDRECEPTOR_ACOUNT`) REFERENCES `account` (`ID_ACCOUNT`),
  ADD CONSTRAINT `FK_TRANSACT_CUENTATRA_ACCOUNT` FOREIGN KEY (`IDEMITTER_ACOUNT`) REFERENCES `account` (`ID_ACCOUNT`),
  ADD CONSTRAINT `FK_TRANSACT_RELATIONS_BANK` FOREIGN KEY (`ID_BANK`) REFERENCES `bank` (`ID_BANK`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
