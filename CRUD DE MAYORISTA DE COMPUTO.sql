-- Base de datos: Mayorista de Cómputo
-- Crear y usar la base de datos
CREATE DATABASE proyecto_crud;

-- Tabla Productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    tipo_producto VARCHAR(100),
    marca VARCHAR(100),
    estatus VARCHAR(50),
    fecha_entrega DATE,
    cantidad INT,
    precio_compra NUMERIC(10,2)
);

-- Tabla Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(200)
);
