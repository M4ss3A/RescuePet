CREATE TABLE usuarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(30),
    direccion VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE usuario_roles (
    usuario_id BIGINT NOT NULL,
    rol_id BIGINT NOT NULL,
    PRIMARY KEY (usuario_id, rol_id),
    CONSTRAINT fk_usuario_roles_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CONSTRAINT fk_usuario_roles_rol
        FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE animales (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100),
    sexo VARCHAR(20),
    edad_aproximada INT,
    tamano VARCHAR(30),
    descripcion TEXT,
    estado VARCHAR(30) NOT NULL,
    fecha_alta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rescates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id BIGINT NOT NULL UNIQUE,
    rescatista_id BIGINT NOT NULL,
    fecha_rescate DATE NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    descripcion TEXT,
    CONSTRAINT fk_rescate_animal
        FOREIGN KEY (animal_id) REFERENCES animales(id),
    CONSTRAINT fk_rescate_rescatista
        FOREIGN KEY (rescatista_id) REFERENCES usuarios(id)
);

CREATE TABLE fotos_animal (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id BIGINT NOT NULL,
    url VARCHAR(500) NOT NULL,
    descripcion VARCHAR(255),
    es_principal BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_foto_animal
        FOREIGN KEY (animal_id) REFERENCES animales(id)
);

CREATE TABLE registros_sanitarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id BIGINT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    descripcion TEXT NOT NULL,
    veterinario VARCHAR(150),
    CONSTRAINT fk_registro_sanitario_animal
        FOREIGN KEY (animal_id) REFERENCES animales(id)
);
