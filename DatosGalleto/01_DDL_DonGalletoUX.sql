-- ---------------------------------------------------------------------------- --
-- Archivo: 01_DDL_DonGalletoUX.sql	                                			--
-- Version: 1.0                                                     			--
-- Autor:   Francisco Javier Rocha Aldana   									--
-- Email:   rochaaldanafcojavier@gmail.com / 21000459@alumnos.utleon.edu.mx		--
-- Fecha de elaboracion: 12-11-2024                                 			--
-- ---------------------------------------------------------------------------- --

	CREATE DATABASE DonGalletoUX;
	GO

	USE DonGalletoUX;
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[usuario](
		 UsuarioId			INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Nombre				VARCHAR(150) NOT NULL
		,Pin				VARCHAR(4) NOT NULL
	);
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[medida](
		 MedidaId			INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Nombre				VARCHAR(15) NOT NULL
	);
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[inventario](
		 InventarioId		INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Nombre				VARCHAR(45) NOT NULL
		,FechaCompra		DATETIME NOT NULL
		,FechaVencimiento	DATETIME NOT NULL
		,Activo				TINYINT NOT NULL
		,Cantidad			DECIMAL(18, 2) NOT NULL
		,Precio				DECIMAL(18, 2) NOT NULL
		,Porcentaje			INT NOT NULL
		,MedidaId			INT NOT NULL

		,FOREIGN KEY (MedidaId) REFERENCES [DonGalletoUX].[dbo].[medida](MedidaId)
	);
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[galleta](
		 GalletaId			INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Nombre				VARCHAR(50) NOT NULL
		,Cantidad			DECIMAL(18, 2) NOT NULL
		,PrecioVenta		DECIMAL(18, 2) NOT NULL
		,PrecioProduccion	DECIMAL(18, 2) NOT NULL
		,Imagen				VARCHAR(MAX) NOT NULL
		,MedidaId			INT NOT NULL

		,FOREIGN KEY (MedidaId) REFERENCES [DonGalletoUX].[dbo].[medida](MedidaId)
	);
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[receta](
		 RecetaId			INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Cantidad			DECIMAL(18, 2) NOT NULL
		,GalletaId			INT NOT NULL
		,InventarioId		INT NOT NULL
		,MedidaId			INT NOT NULL

		,FOREIGN KEY (GalletaId) REFERENCES [DonGalletoUX].[dbo].[galleta](GalletaId)
		,FOREIGN KEY (InventarioId) REFERENCES [DonGalletoUX].[dbo].[inventario](InventarioId)
		,FOREIGN KEY (MedidaId) REFERENCES [DonGalletoUX].[dbo].[medida](MedidaId)
	);
	GO