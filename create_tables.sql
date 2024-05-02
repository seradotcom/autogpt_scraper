-- Creación de la tabla 'logo'
CREATE TABLE logo (
    id_logo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NULL,
    imgdir VARCHAR(255) NULL
);

alter table logo AUTO_INCREMENT = 1;
alter table enterprise_category AUTO_INCREMENT = 1;
alter table content_type AUTO_INCREMENT = 1;
alter table ecosystem_layer AUTO_INCREMENT = 1;
alter table ais AUTO_INCREMENT = 1;
alter table evaluaciones AUTO_INCREMENT = 1;
DELETE FROM logo;
DELETE FROM enterprise_category;
DELETE FROM content_type;
DELETE FROM ecosystem_layer;
DELETE FROM AIs;
DELETE FROM evaluaciones;

-- Creación de la tabla 'enterprise_category'
CREATE TABLE enterprise_category (
    id_enterprise_category INT PRIMARY KEY AUTO_INCREMENT,
    proposito VARCHAR(100) NOT NULL
);

-- Creación de la tabla 'content_type'
CREATE TABLE content_type (
    id_content_type INT PRIMARY KEY AUTO_INCREMENT,
    type_content VARCHAR(45) NOT NULL
);

-- Creación de la tabla 'ecosystem_layer'
CREATE TABLE ecosystem_layer (
    id_ecosystem_layer INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL
);

-- Creación de la tabla 'AIs'
CREATE TABLE AIs (
    id_ais INT PRIMARY KEY AUTO_INCREMENT,
    ai_name VARCHAR(45) NOT NULL,
    descripcion TEXT,
    licencia VARCHAR(45),
    suscripcion VARCHAR(45),
    link VARCHAR(200),
    logo_id_logo INT,
    enterprise_category_id_enterprise_category INT,
    ecosystem_layer_id_ecosystem_layer INT,  -- Nueva columna
    FOREIGN KEY (logo_id_logo) REFERENCES logo(id_logo),
    FOREIGN KEY (enterprise_category_id_enterprise_category) REFERENCES enterprise_category(id_enterprise_category),
    FOREIGN KEY (ecosystem_layer_id_ecosystem_layer) REFERENCES ecosystem_layer(id_ecosystem_layer)  -- Nueva foreign key
);

-- Creación de la tabla 'evaluaciones'
CREATE TABLE evaluaciones (
    id_evaluaciones INT PRIMARY KEY AUTO_INCREMENT,
    calificacion INT,
    comentario LONGTEXT,
    fecha DATETIME,
    AIs_id_ais INT,
    FOREIGN KEY (AIs_id_ais) REFERENCES AIs(id_ais)
);