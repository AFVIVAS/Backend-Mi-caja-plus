-- MiCaja Plus: esquema de base de datos (MySQL 8, utf8mb4).
-- Solo estructura y catálogo base de categorías; sin datos de usuarios.

CREATE DATABASE IF NOT EXISTS `Micajaplus` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `Micajaplus`;

CREATE TABLE `tendero` (
  `cedula` varchar(10) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `llave` varchar(200) NOT NULL,                -- hash Argon2id del teléfono
  `fechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB;

CREATE TABLE `categorias` (
  `idCategorias` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  PRIMARY KEY (`idCategorias`)
) ENGINE=InnoDB;

CREATE TABLE `productos` (                      -- catálogo global
  `idProductos` int NOT NULL AUTO_INCREMENT,
  `idCategorias` int NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `presentacion` varchar(30) NOT NULL,
  PRIMARY KEY (`idProductos`),
  CONSTRAINT `fk_Productos_Categorias` FOREIGN KEY (`idCategorias`) REFERENCES `categorias` (`idCategorias`)
) ENGINE=InnoDB;

CREATE TABLE `diccionarioproductos` (           -- sinónimos para búsqueda
  `idDiccionario` int NOT NULL AUTO_INCREMENT,
  `idProductos` int NOT NULL,
  `sinonimo` varchar(150) NOT NULL,
  PRIMARY KEY (`idDiccionario`),
  CONSTRAINT `fk_Diccionario_Productos` FOREIGN KEY (`idProductos`) REFERENCES `productos` (`idProductos`)
) ENGINE=InnoDB;

CREATE TABLE `inventario` (                     -- inventario propio de cada tendero
  `idInventario` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `cantidad` int NOT NULL,
  `valorVenta` int NOT NULL,
  `valorCompra` int NOT NULL,
  `nombreProducto` varchar(60) NOT NULL,
  `presentacion` varchar(30) NOT NULL,
  `idCategoria` int NOT NULL,
  PRIMARY KEY (`idInventario`),
  CONSTRAINT `fk_Inventario_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`),
  CONSTRAINT `fk_Categoria_Inventario` FOREIGN KEY (`idCategoria`) REFERENCES `categorias` (`idCategorias`)
) ENGINE=InnoDB;

CREATE TABLE `cliente` (
  `idCliente` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `cedula` varchar(10) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `saldo` int NOT NULL DEFAULT 0,               -- deuda actual
  PRIMARY KEY (`idCliente`),
  CONSTRAINT `fk_Cliente_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`)
) ENGINE=InnoDB;

CREATE TABLE `ventas` (
  `idVentas` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `mensaje` text NOT NULL,
  `tipoPago` varchar(9) NOT NULL,               -- 'efectivo' | 'credito'
  `valor` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idVentas`),
  CONSTRAINT `fk_Ventas_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`)
) ENGINE=InnoDB;

CREATE TABLE `creditos` (                       -- ventas fiadas a un cliente
  `idCreditos` int NOT NULL AUTO_INCREMENT,
  `idVentas` int NOT NULL,
  `idCliente` int NOT NULL,
  PRIMARY KEY (`idCreditos`),
  CONSTRAINT `fk_Creditos_Ventas` FOREIGN KEY (`idVentas`) REFERENCES `ventas` (`idVentas`),
  CONSTRAINT `fk_Creditos_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`)
) ENGINE=InnoDB;

CREATE TABLE `abonos` (
  `idAbonos` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `idCliente` int NOT NULL,
  `abono` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idAbonos`),
  CONSTRAINT `fk_Abonos_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`),
  CONSTRAINT `fk_Abonos_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`)
) ENGINE=InnoDB;

CREATE TABLE `costos` (                         -- compras a proveedores
  `idCostos` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `mensaje` text NOT NULL,
  `valor` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `proveedor` varchar(40) NOT NULL,
  PRIMARY KEY (`idCostos`),
  CONSTRAINT `fk_Costos_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`)
) ENGINE=InnoDB;

CREATE TABLE `gastos` (
  `idGastos` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `mensaje` text NOT NULL,
  `valor` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idGastos`),
  CONSTRAINT `fk_Gastos_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`)
) ENGINE=InnoDB;

CREATE TABLE `apertura` (                       -- base de caja inicial
  `idApertura` int NOT NULL AUTO_INCREMENT,
  `idTendero` varchar(10) NOT NULL,
  `baseInicial` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idApertura`),
  CONSTRAINT `fk_Apertura_Tendero` FOREIGN KEY (`idTendero`) REFERENCES `tendero` (`cedula`)
) ENGINE=InnoDB;

INSERT INTO `categorias` (`idCategorias`, `nombre`) VALUES
(1,'abarrotes'),(2,'bebidas'),(3,'dulcería'),(4,'licores'),(5,'fruver'),(6,'lácteos'),
(7,'aseo personal'),(8,'aseo general'),(9,'cárnicos'),(10,'papelería'),(11,'fármacos'),(12,'mascotas');
