-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.37 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para grow_system
CREATE DATABASE IF NOT EXISTS `grow_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `grow_system`;

-- Volcando estructura para tabla grow_system.planta
CREATE TABLE IF NOT EXISTS `planta` (
  `id_planta` int NOT NULL AUTO_INCREMENT,
  `especie` varchar(20) DEFAULT NULL,
  `cajon` int NOT NULL,
  `cantidad_plantines` int NOT NULL,
  PRIMARY KEY (`id_planta`),
  UNIQUE KEY `Índice 3` (`cajon`) USING BTREE,
  UNIQUE KEY `Índice 2` (`especie`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla grow_system.planta: ~4 rows (aproximadamente)
INSERT INTO `planta` (`id_planta`, `especie`, `cajon`, `cantidad_plantines`) VALUES
	(1, 'MALBON', 1, 10),
	(2, 'LAUREL', 2, 10),
	(3, 'Rosa Blanca', 3, 10),
	(7, 'jazmin', 4, 10);

-- Volcando estructura para tabla grow_system.riego
CREATE TABLE IF NOT EXISTS `riego` (
  `planta` int NOT NULL,
  `fecha_ultimo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `riego_auto` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'habilitado',
  KEY `planta` (`planta`),
  CONSTRAINT `riego_ibfk_1` FOREIGN KEY (`planta`) REFERENCES `planta` (`id_planta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla grow_system.riego: ~4 rows (aproximadamente)
INSERT INTO `riego` (`planta`, `fecha_ultimo`, `riego_auto`) VALUES
	(1, '22-10-2024', 'habilitado'),
	(1, '22-10-2024', 'habilitado'),
	(3, '22-10-2024', 'habilitado'),
	(7, '22-10-2024', 'habilitado');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
