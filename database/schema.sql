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

CREATE TABLE hogares_transito (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    responsable_id BIGINT NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    capacidad INT NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    CONSTRAINT fk_hogar_responsable
        FOREIGN KEY (responsable_id) REFERENCES usuarios(id)
);

CREATE TABLE asignaciones_transito (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id BIGINT NOT NULL,
    hogar_transito_id BIGINT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE,
    observaciones TEXT,
    CONSTRAINT fk_asignacion_animal
        FOREIGN KEY (animal_id) REFERENCES animales(id),
    CONSTRAINT fk_asignacion_hogar
        FOREIGN KEY (hogar_transito_id) REFERENCES hogares_transito(id)
);

CREATE TABLE publicaciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id BIGINT NOT NULL,
    autor_id BIGINT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_publicacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) NOT NULL,
    CONSTRAINT fk_publicacion_animal
        FOREIGN KEY (animal_id) REFERENCES animales(id),
    CONSTRAINT fk_publicacion_autor
        FOREIGN KEY (autor_id) REFERENCES usuarios(id)
);

CREATE TABLE solicitudes_adopcion (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id BIGINT NOT NULL,
    adoptante_id BIGINT NOT NULL,
    fecha_solicitud DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) NOT NULL,
    tipo_vivienda VARCHAR(50) NOT NULL,
    tiene_patio BOOLEAN NOT NULL,
    tiene_otros_animales BOOLEAN NOT NULL,
    experiencia_previa TEXT,
    motivo TEXT NOT NULL,
    puntaje_compatibilidad DECIMAL(5,2),
    CONSTRAINT fk_solicitud_publicacion
        FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id),
    CONSTRAINT fk_solicitud_adoptante
        FOREIGN KEY (adoptante_id) REFERENCES usuarios(id)
);

CREATE TABLE adopciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    solicitud_id BIGINT NOT NULL UNIQUE,
    fecha_adopcion DATE NOT NULL,
    estado VARCHAR(30) NOT NULL,
    observaciones TEXT,
    CONSTRAINT fk_adopcion_solicitud
        FOREIGN KEY (solicitud_id) REFERENCES solicitudes_adopcion(id)
);

CREATE TABLE seguimientos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    adopcion_id BIGINT NOT NULL,
    fecha DATE NOT NULL,
    observaciones TEXT,
    estado_general VARCHAR(100),
    resultado VARCHAR(100),
    CONSTRAINT fk_seguimiento_adopcion
        FOREIGN KEY (adopcion_id) REFERENCES adopciones(id)
);

-- Indices Principales

CREATE INDEX idx_usuario_roles_rol
    ON usuario_roles (rol_id);

CREATE INDEX idx_animales_estado
    ON animales (estado);

CREATE INDEX idx_registros_sanitarios_animal_fecha
    ON registros_sanitarios (animal_id, fecha);

CREATE INDEX idx_hogares_transito_disponible
    ON hogares_transito (disponible);

CREATE INDEX idx_asignaciones_animal_salida
    ON asignaciones_transito (animal_id, fecha_salida);

CREATE INDEX idx_publicaciones_estado_fecha
    ON publicaciones (estado, fecha_publicacion);

CREATE INDEX idx_solicitudes_publicacion_estado
    ON solicitudes_adopcion (publicacion_id, estado);

CREATE INDEX idx_solicitudes_adoptante_estado
    ON solicitudes_adopcion (adoptante_id, estado);

CREATE INDEX idx_seguimientos_adopcion_fecha
    ON seguimientos (adopcion_id, fecha);
