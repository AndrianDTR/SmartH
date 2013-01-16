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

grant all on therm.* to 'therm'@'localhost' identified by 'therm';

-- Dumping database structure for therm
DROP DATABASE IF EXISTS `therm`;
CREATE DATABASE IF NOT EXISTS `therm` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `therm`;


-- Dumping structure for table therm.DeviceTypes
DROP TABLE IF EXISTS `DeviceTypes`;
CREATE TABLE IF NOT EXISTS `DeviceTypes` (
  `Code` int(10) unsigned NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.1wSensors: ~0 rows (approximately)
DELETE FROM `DeviceTypes`;
insert into `DeviceTypes`(`Code`,`Name`) values(28,'DS18B20'),(24,'DS2413');
/*!40000 ALTER TABLE `DeviceTypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `DeviceTypes` ENABLE KEYS */;

-- Dumping structure for table therm.1wDevices
DROP TABLE IF EXISTS `1wDevices`;
CREATE TABLE IF NOT EXISTS `1wDevices` (
  `Type` int(10) unsigned,
  `Id` bigint(20) unsigned,
  `Name` varchar(50) DEFAULT NULL,
  `Direction` enum('In', 'Out') DEFAULT 'In',
  KEY `Type` (`Type`,`Id`),
  KEY `FK_DeviceType_1wDevice` (`Type`),
  CONSTRAINT `FK_DeviceType_1wDevice` FOREIGN KEY (`Type`) REFERENCES `DeviceTypes` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.1wSensors: ~0 rows (approximately)
DELETE FROM `1wDevices`;
/*!40000 ALTER TABLE `1wDevices` DISABLE KEYS */;
/*!40000 ALTER TABLE `1wDevices` ENABLE KEYS */;

-- Dumping structure for table therm.SensorValues
DROP TABLE IF EXISTS `DeviceValues`;
CREATE TABLE IF NOT EXISTS `DeviceValues` (
  `Type` int(10) unsigned,
  `DeviceId` bigint(20) unsigned,
  `TimeMark` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Value` int(10) unsigned DEFAULT NULL,
  KEY `TimeMark` (`TimeMark`,`DeviceId`),
  KEY `FK_DeviceValuesDeviceId_1wDevices` (`DeviceId`,`Type`),
  CONSTRAINT `FK_DeviceValuesDeviceId_1wDevices` FOREIGN KEY (`DeviceId`) REFERENCES `1wDevices` (`Id`),
  CONSTRAINT `FK_DeviceValuesType_1wDevices` FOREIGN KEY (`Type`) REFERENCES `1wDevices` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.SensorValues: ~0 rows (approximately)
DELETE FROM `DeviceValues`;
/*!40000 ALTER TABLE `DeviceValues` DISABLE KEYS */;
/*!40000 ALTER TABLE `DeviceValues` ENABLE KEYS */;


-- Dumping structure for table therm.SwitchsState
DROP TABLE IF EXISTS `DevicesState`;
CREATE TABLE IF NOT EXISTS `DevicesState` (
  `Id` bigint(20) unsigned DEFAULT NULL,
  `Value` int(10) DEFAULT NULL,
  UNIQUE KEY `Id` (`Id`),
  CONSTRAINT `FK_DevicesState_1wDevices` FOREIGN KEY (`Id`) REFERENCES `1wDevices` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table therm.SwitchsState: ~0 rows (approximately)
DELETE FROM `DevicesState`;
/*!40000 ALTER TABLE `DevicesState` DISABLE KEYS */;
/*!40000 ALTER TABLE `DevicesState` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
