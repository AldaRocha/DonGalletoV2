-- ---------------------------------------------------------------------------- --
-- Archivo: 01_DDL_DonGalletoUX.sql	                                			--
-- Version: 1.0                                                     			--
-- Autor:   Francisco Javier Rocha Aldana   									--
-- Email:   rochaaldanafcojavier@gmail.com / 21000459@alumnos.utleon.edu.mx		--
-- Fecha de elaboracion: 12-11-2024                                 			--
-- ---------------------------------------------------------------------------- --

--	Script de inicio

	CREATE DATABASE DonGalletoUX;
	GO

	USE DonGalletoUX;
	GO

	CREATE TABLE [DonGalletoUX].[dbo].[usuario](
		 UsuarioId	INT NOT NULL PRIMARY KEY IDENTITY(1, 1)
		,Nombre		VARCHAR(150) NOT NULL
		,Pin		VARCHAR(4) NOT NULL
	);
	GO

	INSERT INTO [DonGalletoUX].[dbo].[usuario](Nombre, Pin) VALUES('Don Galleto', '1234');
	GO