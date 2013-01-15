-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.28-0ubuntu0.12.04.3 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2013-01-15 16:22:19
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping database structure for therm
DROP DATABASE IF EXISTS `therm`;
CREATE DATABASE IF NOT EXISTS `therm` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `therm`;


-- Dumping structure for table therm.1wSensors
DROP TABLE IF EXISTS `1wSensors`;
CREATE TABLE IF NOT EXISTS `1wSensors` (
  `Id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `Name` varchar(50) DEFAULT NULL,
  `Type` int(10) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.1wSensors: ~0 rows (approximately)
DELETE FROM `1wSensors`;
/*!40000 ALTER TABLE `1wSensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `1wSensors` ENABLE KEYS */;


-- Dumping structure for table therm.1wSwitchs
DROP TABLE IF EXISTS `1wSwitchs`;
CREATE TABLE IF NOT EXISTS `1wSwitchs` (
  `Id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `Name` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `Type` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.1wSwitchs: ~0 rows (approximately)
DELETE FROM `1wSwitchs`;
/*!40000 ALTER TABLE `1wSwitchs` DISABLE KEYS */;
/*!40000 ALTER TABLE `1wSwitchs` ENABLE KEYS */;


-- Dumping structure for table therm.SensorValues
DROP TABLE IF EXISTS `SensorValues`;
CREATE TABLE IF NOT EXISTS `SensorValues` (
  `SensorId` bigint(20) unsigned DEFAULT NULL,
  `TimeMark` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Value` timestamp NULL DEFAULT NULL,
  KEY `TimeMark` (`TimeMark`,`SensorId`),
  KEY `FK_SensorValues_1wSensors` (`SensorId`),
  CONSTRAINT `FK_SensorValues_1wSensors` FOREIGN KEY (`SensorId`) REFERENCES `1wSensors` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.SensorValues: ~0 rows (approximately)
DELETE FROM `SensorValues`;
/*!40000 ALTER TABLE `SensorValues` DISABLE KEYS */;
/*!40000 ALTER TABLE `SensorValues` ENABLE KEYS */;


-- Dumping structure for table therm.SwitchsState
DROP TABLE IF EXISTS `SwitchsState`;
CREATE TABLE IF NOT EXISTS `SwitchsState` (
  `Id` bigint(20) unsigned DEFAULT NULL,
  `Value` int(10) DEFAULT NULL,
  UNIQUE KEY `Id` (`Id`),
  CONSTRAINT `FK_SwitchsState_1wSwitchs` FOREIGN KEY (`Id`) REFERENCES `1wSwitchs` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.SwitchsState: ~0 rows (approximately)
DELETE FROM `SwitchsState`;
/*!40000 ALTER TABLE `SwitchsState` DISABLE KEYS */;
/*!40000 ALTER TABLE `SwitchsState` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
