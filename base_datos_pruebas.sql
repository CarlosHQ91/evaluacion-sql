-- ============================================================
-- BASE DE DATOS DE PRUEBAS PARA EVALUACIÓN PRÁCTICA
-- Asignatura: Auditoría de Sistemas Informáticos
-- Tema: Seguridad lógica en bases de datos MySQL
-- ============================================================

-- ============================================================
-- PASO 1: CREAR LA BASE DE DATOS
-- ============================================================
DROP DATABASE IF EXISTS empresa_auditoria;
CREATE DATABASE empresa_auditoria
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE empresa_auditoria;

-- ============================================================
-- PASO 2: CREAR TABLAS
-- ============================================================

-- Tabla de departamentos
CREATE TABLE departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    presupuesto DECIMAL(12,2),
    fecha_creacion DATE DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB;

-- Tabla de empleados (contiene datos "sensibles")
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    primer_nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    dui VARCHAR(10),  -- Documento de identidad (dato sensible)
    fecha_contratacion DATE NOT NULL,
    id_departamento INT,
    cargo VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
) ENGINE=InnoDB;

-- Tabla de salarios (información confidencial)
CREATE TABLE salarios (
    id_salario INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    salario_base DECIMAL(10,2) NOT NULL,
    bonificacion DECIMAL(10,2) DEFAULT 0.00,
    deducciones DECIMAL(10,2) DEFAULT 0.00,
    fecha_efectiva DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
) ENGINE=InnoDB;

-- Tabla de proyectos
CREATE TABLE proyectos (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin_estimada DATE,
    presupuesto DECIMAL(12,2),
    estado ENUM('planificacion', 'en_progreso', 'completado', 'cancelado') DEFAULT 'planificacion',
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
) ENGINE=InnoDB;

-- Tabla de asignaciones empleado-proyecto
CREATE TABLE asignaciones (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    id_proyecto INT NOT NULL,
    rol_en_proyecto VARCHAR(100),
    fecha_asignacion DATE DEFAULT (CURRENT_DATE),
    horas_semanales INT DEFAULT 40,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
) ENGINE=InnoDB;

-- Tabla de registro de accesos (para ejercicios de auditoría)
CREATE TABLE log_accesos (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100),
    accion VARCHAR(50),
    tabla_afectada VARCHAR(100),
    descripcion TEXT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- PASO 3: INSERTAR DATOS DE PRUEBA
-- ============================================================

-- Departamentos
INSERT INTO departamentos (nombre, ubicacion, presupuesto) VALUES
('Tecnología de la Información', 'Edificio A, Piso 3', 150000.00),
('Recursos Humanos', 'Edificio A, Piso 1', 80000.00),
('Contabilidad y Finanzas', 'Edificio B, Piso 2', 120000.00),
('Ventas y Mercadeo', 'Edificio B, Piso 1', 95000.00),
('Gerencia General', 'Edificio A, Piso 4', 200000.00);

-- Empleados (datos ficticios)
INSERT INTO empleados (primer_nombre, apellido, email, telefono, dui, fecha_contratacion, id_departamento, cargo) VALUES
('María', 'González Pérez', 'mgonzalez@empresa.com', '7000-1001', '01234567-8', '2020-03-15', 1, 'Jefa de TI'),
('Juan', 'Martínez López', 'jmartinez@empresa.com', '7000-1002', '02345678-9', '2019-06-20', 1, 'Administrador de Base de Datos'),
('Ana', 'Hernández Rivera', 'ahernandez@empresa.com', '7000-1003', '03456789-0', '2021-01-10', 2, 'Coordinadora de RRHH'),
('Carlos', 'López Castillo', 'clopez@empresa.com', '7000-1004', '04567890-1', '2018-09-01', 3, 'Contador General'),
('Laura', 'Ramírez Díaz', 'lramirez@empresa.com', '7000-1005', '05678901-2', '2022-02-14', 4, 'Ejecutiva de Ventas'),
('Roberto', 'Flores Mendoza', 'rflores@empresa.com', '7000-1006', '06789012-3', '2017-11-03', 5, 'Gerente General'),
('Patricia', 'Torres Vega', 'ptorres@empresa.com', '7000-1007', '07890123-4', '2021-07-22', 1, 'Desarrolladora'),
('Fernando', 'Morales Cruz', 'fmorales@empresa.com', '7000-1008', '08901234-5', '2020-05-18', 3, 'Asistente Contable'),
('Sandra', 'Reyes Guzmán', 'sreyes@empresa.com', '7000-1009', '09012345-6', '2023-01-09', 2, 'Analista de RRHH'),
('Diego', 'Vargas Portillo', 'dvargas@empresa.com', '7000-1010', '10123456-7', '2022-08-30', 4, 'Gerente de Ventas'),
('Claudia', 'Mejía Alfaro', 'cmejia@empresa.com', '7000-1011', '11234567-8', '2019-04-12', 1, 'Analista de Seguridad'),
('Pedro', 'Aguilar Santos', 'paguilar@empresa.com', '7000-1012', '12345678-9', '2023-06-01', 3, 'Auditor Interno');

-- Salarios (información confidencial)
INSERT INTO salarios (id_empleado, salario_base, bonificacion, deducciones, fecha_efectiva) VALUES
(1, 2500.00, 300.00, 250.00, '2024-01-01'),
(2, 2200.00, 200.00, 220.00, '2024-01-01'),
(3, 1800.00, 150.00, 180.00, '2024-01-01'),
(4, 2000.00, 250.00, 200.00, '2024-01-01'),
(5, 1500.00, 500.00, 150.00, '2024-01-01'),
(6, 3500.00, 500.00, 350.00, '2024-01-01'),
(7, 1800.00, 100.00, 180.00, '2024-01-01'),
(8, 1200.00, 50.00, 120.00, '2024-01-01'),
(9, 1400.00, 100.00, 140.00, '2024-01-01'),
(10, 2300.00, 400.00, 230.00, '2024-01-01'),
(11, 2100.00, 200.00, 210.00, '2024-01-01'),
(12, 1900.00, 150.00, 190.00, '2024-01-01');

-- Proyectos
INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin_estimada, presupuesto, estado, id_departamento) VALUES
('Migración de Servidores', 'Migración de servidores físicos a infraestructura en la nube', '2024-01-15', '2024-06-30', 45000.00, 'en_progreso', 1),
('Sistema de Nómina v2', 'Actualización del sistema de gestión de nómina', '2024-02-01', '2024-08-31', 30000.00, 'en_progreso', 1),
('Auditoría Financiera 2024', 'Revisión integral de estados financieros', '2024-03-01', '2024-05-31', 15000.00, 'planificacion', 3),
('Campaña de Ventas Q2', 'Campaña de mercadeo para el segundo trimestre', '2024-04-01', '2024-06-30', 20000.00, 'planificacion', 4);

-- Asignaciones
INSERT INTO asignaciones (id_empleado, id_proyecto, rol_en_proyecto, horas_semanales) VALUES
(1, 1, 'Líder del Proyecto', 20),
(2, 1, 'DBA - Migración de datos', 40),
(7, 1, 'Desarrolladora de scripts', 30),
(11, 1, 'Seguridad y accesos', 15),
(2, 2, 'DBA - Diseño de esquema', 20),
(7, 2, 'Desarrolladora principal', 35),
(4, 3, 'Responsable contable', 30),
(8, 3, 'Apoyo en documentación', 40),
(12, 3, 'Auditor asignado', 40),
(5, 4, 'Ejecutiva de campaña', 35),
(10, 4, 'Director de campaña', 20);

-- Registros de ejemplo en log_accesos
INSERT INTO log_accesos (usuario, accion, tabla_afectada, descripcion) VALUES
('root', 'LOGIN', NULL, 'Inicio de sesión desde localhost'),
('root', 'CREATE', 'empleados', 'Creación de tabla empleados'),
('root', 'INSERT', 'empleados', 'Carga inicial de 12 registros'),
('root', 'INSERT', 'salarios', 'Carga inicial de datos salariales'),
('root', 'GRANT', NULL, 'Asignación de privilegios pendiente');

-- ============================================================
-- PASO 4: CREAR USUARIOS PARA EJERCICIOS (OPCIONAL)
-- Descomente las líneas siguientes si desea pre-crear
-- los usuarios antes de la evaluación.
-- ============================================================

/*
-- Usuario auditor: solo lectura
CREATE USER 'auditor'@'localhost' IDENTIFIED BY 'Aud1t0r_2024!';
GRANT SELECT ON empresa_auditoria.* TO 'auditor'@'localhost';

-- Usuario operador: lectura y escritura limitada
CREATE USER 'operador'@'localhost' IDENTIFIED BY 'Op3rad0r_2024!';
GRANT SELECT, INSERT, UPDATE ON empresa_auditoria.empleados TO 'operador'@'localhost';
GRANT SELECT, INSERT, UPDATE ON empresa_auditoria.asignaciones TO 'operador'@'localhost';
GRANT SELECT ON empresa_auditoria.departamentos TO 'operador'@'localhost';
GRANT SELECT ON empresa_auditoria.proyectos TO 'operador'@'localhost';

-- Usuario consulta_rrhh: solo lectura en empleados (sin salarios)
CREATE USER 'consulta_rrhh'@'localhost' IDENTIFIED BY 'Rrhh_2024!';
GRANT SELECT ON empresa_auditoria.empleados TO 'consulta_rrhh'@'localhost';
GRANT SELECT ON empresa_auditoria.departamentos TO 'consulta_rrhh'@'localhost';

-- Rol de solo consulta
CREATE ROLE 'rol_consulta';
GRANT SELECT ON empresa_auditoria.* TO 'rol_consulta';

FLUSH PRIVILEGES;
*/

-- ============================================================
-- VERIFICACIÓN RÁPIDA
-- ============================================================
SELECT 'Base de datos empresa_auditoria creada exitosamente' AS mensaje;
SELECT COUNT(*) AS total_empleados FROM empleados;
SELECT COUNT(*) AS total_departamentos FROM departamentos;
SELECT COUNT(*) AS total_salarios FROM salarios;
SELECT COUNT(*) AS total_proyectos FROM proyectos;
