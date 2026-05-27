CREATE DATABASE IF NOT EXISTS cafeteria;
USE cafeteria;

CREATE TABLE IF NOT EXISTS franjas_horarias(
    id_franja INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    dia_semana INT NOT NULL,
    hora_apertura TIME DEFAULT '09:00:00',
    hora_cierre TIME DEFAULT '20:00:00',
    capacidad_maxima INT NOT NULL,
    capacidad_ocupada INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS reservas(
    id_reserva INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_usuario INT NOT NULL,
    id_franja INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    fecha_creacion DATETIME DEFAULT current_timestamp(),
    cantidad_personas INT NOT NULL DEFAULT 1,
    alergias JSON,
    servicios JSON,
    observaciones VARCHAR(100),
    estado ENUM(
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Completada"
    ) DEFAULT "Pendiente",
    qr VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_usuario)
    REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_franja)
    REFERENCES franjas_horarias (id_franja)
);

CREATE TABLE IF NOT EXISTS resenas(
    id_resena INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_reserva INT NOT NULL,
    estrellas INT NOT NULL,
    comentario VARCHAR(300) NOT NULL,
    fecha DATETIME DEFAULT current_timestamp(),
    FOREIGN KEY (id_reserva)
    REFERENCES reservas (id_reserva)
);

CREATE TABLE IF NOT EXISTS servicios(
    id_servicio INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS menu(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(300) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    tags JSON,
    imagen VARCHAR(150) NOT NULL,
    activo BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS administrador(
    id_admin INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usuario VARCHAR(30) NOT NULL UNIQUE,
    contrasenia VARCHAR(255) NOT NULL
);