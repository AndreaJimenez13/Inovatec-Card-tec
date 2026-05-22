-- Crear la base de datos
CREATE DATABASE CardTec;
GO

USE CardTec;
GO

-- Tabla: Usuario
CREATE TABLE Usuario (
    no_control      INT             NOT NULL,
    nombre_usuario  VARCHAR(50)     NOT NULL,
    rol             VARCHAR(10)     NOT NULL CHECK (rol IN ('Alumno', 'Docente', 'Admin')),
    estado          VARCHAR(12)     NOT NULL CHECK (estado IN ('Activo', 'Suspendido')),
    CONSTRAINT PK_Usuario PRIMARY KEY (no_control)
);
GO

-- Tabla: Credenciales (relación 1:1 con Usuario)
CREATE TABLE Credenciales (
    RFID_UID        VARCHAR(20)     NOT NULL,
    no_control      INT             NOT NULL,
    fecha_emision   DATE            NOT NULL,
    CONSTRAINT PK_Credenciales     PRIMARY KEY (RFID_UID),
    CONSTRAINT FK_Cred_Usuario     FOREIGN KEY (no_control)
        REFERENCES Usuario(no_control),
    CONSTRAINT UQ_Cred_NoControl   UNIQUE (no_control)
);
GO

-- Tabla: Puntos_acceso
CREATE TABLE Puntos_acceso (
    id_puntos_acceso    INT             NOT NULL IDENTITY(1,1),
    nombre_ubicacion    VARCHAR(100)    NOT NULL,
    nivel_seguridad     VARCHAR(20)     NOT NULL,
    CONSTRAINT PK_PuntosAcceso PRIMARY KEY (id_puntos_acceso)
);
GO

-- Tabla: Historial_acceso
CREATE TABLE Historial_acceso (
    id_historial_acceso INT         NOT NULL IDENTITY(1,1),
    RFID_UID            VARCHAR(20) NOT NULL,
    id_puntos_acceso    INT         NOT NULL,
    fecha               DATE        NOT NULL,
    hora                TIME        NOT NULL,
    acceso_concedido    BIT         NOT NULL,
    CONSTRAINT PK_Historial         PRIMARY KEY (id_historial_acceso),
    CONSTRAINT FK_Hist_Credencial   FOREIGN KEY (RFID_UID)
        REFERENCES Credenciales(RFID_UID),
    CONSTRAINT FK_Hist_Punto        FOREIGN KEY (id_puntos_acceso)
        REFERENCES Puntos_acceso(id_puntos_acceso)
);
GO






USE CardTec;
GO

-- Eliminar tablas en orden (primero las que tienen FK)
DROP TABLE IF EXISTS Historial_acceso;
DROP TABLE IF EXISTS Credenciales;
DROP TABLE IF EXISTS Puntos_acceso;
DROP TABLE IF EXISTS Usuario;
GO

-- Tabla: Usuario
CREATE TABLE Usuario (
    no_control      INT             NOT NULL,
    nombre_usuario  VARCHAR(50)     NOT NULL,
    rol             VARCHAR(10)     NOT NULL CHECK (rol IN ('Alumno', 'Docente', 'Admin')),
    estado          VARCHAR(12)     NOT NULL CHECK (estado IN ('Activo', 'Suspendido')),
    CONSTRAINT PK_Usuario PRIMARY KEY (no_control)
);
GO

-- Tabla: Credenciales (relación 1:1 con Usuario)
CREATE TABLE Credenciales (
    RFID_UID        VARCHAR(20)     NOT NULL,
    no_control      INT             NOT NULL,
    fecha_emision   DATE            NOT NULL,
    CONSTRAINT PK_Credenciales     PRIMARY KEY (RFID_UID),
    CONSTRAINT FK_Cred_Usuario     FOREIGN KEY (no_control)
        REFERENCES Usuario(no_control),
    CONSTRAINT UQ_Cred_NoControl   UNIQUE (no_control)
);
GO

-- Tabla: Puntos_acceso
CREATE TABLE Puntos_acceso (
    id_puntos_acceso    INT             NOT NULL IDENTITY(1,1),
    nombre_ubicacion    VARCHAR(100)    NOT NULL,
    nivel_seguridad     VARCHAR(20)     NOT NULL,
    CONSTRAINT PK_PuntosAcceso PRIMARY KEY (id_puntos_acceso)
);
GO

-- Tabla: Historial_acceso
CREATE TABLE Historial_acceso (
    id_historial_acceso INT         NOT NULL IDENTITY(1,1),
    RFID_UID            VARCHAR(20) NOT NULL,
    id_puntos_acceso    INT         NOT NULL,
    fecha               DATE        NOT NULL,
    hora                TIME        NOT NULL,
    acceso_concedido    BIT         NOT NULL,
    CONSTRAINT PK_Historial         PRIMARY KEY (id_historial_acceso),
    CONSTRAINT FK_Hist_Credencial   FOREIGN KEY (RFID_UID)
        REFERENCES Credenciales(RFID_UID),
    CONSTRAINT FK_Hist_Punto        FOREIGN KEY (id_puntos_acceso)
        REFERENCES Puntos_acceso(id_puntos_acceso)
);
GO