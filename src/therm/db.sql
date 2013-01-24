-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.28-0ubuntu0.12.04.3 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2013-01-17 12:06:10
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping database structure for therm
DROP DATABASE IF EXISTS `therm`;
CREATE DATABASE IF NOT EXISTS `therm` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `therm`;

grant all on therm.* to 'therm'@'localhost' identified by 'therm';

-- Dumping structure for table therm.DeviceTypes
DROP TABLE IF EXISTS `DeviceTypes`;
CREATE TABLE IF NOT EXISTS `DeviceTypes` (
  `Code` int(10) unsigned NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Direction` enum('In','Out','Both') DEFAULT 'In',
  PRIMARY KEY (`Code`),
  UNIQUE KEY `Code` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.DeviceTypes: ~2 rows (approximately)
DELETE FROM `DeviceTypes`;
/*!40000 ALTER TABLE `DeviceTypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `DeviceTypes` ENABLE KEYS */;

-- Dumping structure for table therm.1wDevices
DROP TABLE IF EXISTS `1wDevices`;
CREATE TABLE IF NOT EXISTS `1wDevices` (
  `Type` int(10) unsigned DEFAULT NULL,
  `DeviceId` bigint(20) unsigned DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  KEY `Type` (`Type`,`DeviceId`),
  KEY `FK_DeviceType_1wDevice` (`Type`),
  CONSTRAINT `FK_DeviceType_1wDevice` FOREIGN KEY (`Type`) REFERENCES `DeviceTypes` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.1wDevices: ~0 rows (approximately)
DELETE FROM `1wDevices`;
/*!40000 ALTER TABLE `1wDevices` DISABLE KEYS */;
/*!40000 ALTER TABLE `1wDevices` ENABLE KEYS */;

-- Dumping structure for table therm.DevicesState
DROP TABLE IF EXISTS `DevicesState`;
CREATE TABLE IF NOT EXISTS `DevicesState` (
  `Key` int(10) unsigned NOT NULL,
  `DeviceId` bigint(20) unsigned NOT NULL,
  `Value` int(10) DEFAULT NULL,
  UNIQUE KEY `Id` (`DeviceId`),
  KEY `FK_DevicesState_1wDevices` (`Key`,`DeviceId`),
  CONSTRAINT `FK_DevicesState_1wDevices` FOREIGN KEY (`Key`, `DeviceId`) REFERENCES `1wDevices` (`Type`, `DeviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.DevicesState: ~0 rows (approximately)
DELETE FROM `DevicesState`;
/*!40000 ALTER TABLE `DevicesState` DISABLE KEYS */;
/*!40000 ALTER TABLE `DevicesState` ENABLE KEYS */;

-- Dumping structure for table therm.DeviceValues
DROP TABLE IF EXISTS `DeviceValues`;
CREATE TABLE IF NOT EXISTS `DeviceValues` (
  `Type` int(10) unsigned DEFAULT NULL,
  `DeviceId` bigint(20) unsigned DEFAULT NULL,
  `TimeMark` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Value` int(10) unsigned DEFAULT NULL,
  KEY `FK_DeviceValues_1wDevices` (`Type`,`DeviceId`),
  CONSTRAINT `FK_DeviceValues_1wDevices` FOREIGN KEY (`Type`, `DeviceId`) REFERENCES `1wDevices` (`Type`, `DeviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.DeviceValues: ~0 rows (approximately)
DELETE FROM `DeviceValues`;
/*!40000 ALTER TABLE `DeviceValues` DISABLE KEYS */;
/*!40000 ALTER TABLE `DeviceValues` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
