# 🛡️ SQL Audit Quest — Sistema de Evaluación Interactiva

Plataforma web de evaluación en tiempo real sobre **Seguridad Lógica en Bases de Datos (MySQL 8.0)** para la asignatura de **Auditoría de Sistemas Informáticos**.

Diseñada para permitir que un grupo completo de estudiantes realice su examen oficial de forma simultánea, con corrección automática, efectos interactivos, protección anti-reintentos y un panel de control en vivo para el docente.

---

## ✨ Características Principales

### 👨‍🎓 Para los Estudiantes (Modo Examen Oficial)
* **Ingreso Directo y Seguro:** Registro únicamente con Nombre Completo y Carné Universitario.
* **30 Preguntas de Evaluación:** Cubriendo 11 ejes temáticos clave de auditoría y directivas de seguridad en MySQL.
* **Diseño Neumórfico (Soft UI):** Estética visual moderna basada en superficies extruidas 3D, sombras suaves y componentes táctiles.
* **Retroalimentación Interactiva:**
  * 🎉 **Acierto:** Lluvia de confeti verde esmeralda y arpegio sonoro ascendente.
  * 🏴‍☠️ **Fallo:** Animación de temblor cómica y aparición en modal rotativo de los **10 miembros de la tripulación de los Sombrero de Paja (Mugiwara Crew: Luffy, Zoro, Nami, Usopp, Sanji, Chopper, Robin, Franky, Brook y Jinbe)**, cada uno con su avatar SVG exclusivo, efectos sonoros sintetizados y más de 65 frases cómicas alusivas a One Piece y a los errores de auditoría SQL, indicando siempre la opción correcta con fines pedagógicos.
* **Protección Anti-F5 (Auto-Reanudación):** Si el alumno recarga la página o se desconecta, el sistema restaura su examen exactamente en la pregunta donde iba, manteniendo bloqueadas las anteriores.
* **Bloqueo de Reintentos:** Una vez finalizado el examen, el carné queda bloqueado en el servidor para evitar que el estudiante repita la prueba.

---

### 👨‍🏫 Para el Docente (Panel de Control en Vivo)
* **Acceso Protegido:** Ingreso exclusivo mediante PIN maestro en la ruta `/docente`.
* **Métricas en Tiempo Real:**
  * Total de alumnos evaluados.
  * Promedio grupal de calificaciones (escala de 0.0 a 10.0).
  * Nota más alta registrada.
  * Tasa de aprobación grupal ($\ge 6.0$).
* **Monitoreo Simultáneo:** Tabla que se actualiza automáticamente cada 4 segundos con las entregas de los estudiantes.
* **Revisión Individual Detallada:** Botón para examinar pregunta por pregunta las respuestas de cada alumno (mostrando aciertos en verde y fallos en rojo).
* **Gestión de Reintentos:** Botón `🔓 Reintento` para autorizar a un estudiante específico a repetir su prueba en caso de fallas técnicas justificadas.
* **Exportación a Excel:** Descarga de listado completo en formato `.csv` (codificación UTF-8 BOM compatible con Microsoft Excel).

---

## 📚 Ejes Temáticos Evaluados (30 Preguntas)

1. Conceptos Fundamentales de Seguridad Lógica (Autenticación, Mínimo Privilegio, Inyección SQL).
2. Conexión y Reconocimiento del Entorno MySQL.
3. Bases de Datos del Sistema (`mysql`, `information_schema`, `performance_schema`, `sys`).
4. Revisión de Cuentas de Usuario y Riesgo en Hosts (`%`, `localhost`).
5. Base de Datos de Práctica (`empresa_auditoria`) y Datos Sensibles.
6. Creación de Usuarios y Asignación de Privilegios (`GRANT`, `REVOKE`).
7. Uso y Ventajas de Roles en MySQL 8.0.
8. Contraseñas Seguras y Políticas de Expiración (`PASSWORD EXPIRE INTERVAL`).
9. Cifrado de Conexión en Tránsito (TLS/SSL).
10. Registros de Auditoría (`general_log`, `binary_log`, `error_log`).
11. Respaldos Lógicos (`mysqldump`), Restauración y Limpieza del Servidor.

---

## 🛠️ Tecnologías Empleadas

* **Backend:** Python 3 (servidor multihilo `ThreadingHTTPServer` para alta concurrencia).
* **Frontend:** HTML5 semántico, CSS3 Neumórfico puro (sin dependencias externas) y JavaScript vanilla.
* **Audio:** Web Audio API nativa (síntesis de tonos sin necesidad de descargar archivos `.mp3`).
* **Gráficos:** SVG interactivo y Canvas HTML5 para partículas de confeti.
* **Almacenamiento:** Base de datos local en JSON (`resultados_evaluacion.json`).

---

## 🚀 Despliegue y Ejecución

### Opción A: Ejecución Local en Laboratorio / Red del Aula
1. Clona o descarga este repositorio:
   ```bash
   git clone https://github.com/CarlosHQ91/evaluacion-sql.git
   cd evaluacion-sql
   ```
2. Inicia el servidor haciendo doble clic en **`INICIAR_EVALUACION.bat`** o ejecuta en la terminal:
   ```bash
   python servidor_evaluacion.py
   ```
3. El servidor mostrará la IP local asignada (por ejemplo `http://192.168.1.50:8000/`) para compartirla con los estudiantes en la misma red Wi-Fi o red cableada.

---

### Opción B: Despliegue en la Nube (Render.com)
1. Ve a **[Render.com](https://dashboard.render.com/)** e inicia sesión con GitHub.
2. Crea un **New Web Service** y conecta este repositorio: `CarlosHQ91/evaluacion-sql`.
3. Configuración del servicio:
   * **Language:** `Python 3`
   * **Start Command:** `python servidor_evaluacion.py`
   * **Instance Type:** `Free`
4. Render generará automáticamente una URL segura (`https://evaluacion-sql-xxxx.onrender.com`).

---

## 🔐 Credenciales del Docente

* **Ruta de Acceso:** `/docente`
* **PIN Maestro:** `Carlos.26` *(configurable en `servidor_evaluacion.py`)*

---

## 📁 Estructura del Repositorio

```text
evaluacion-sql/
├── servidor_evaluacion.py      # Servidor multihilo HTTP, API y lógica de negocio
├── preguntas.json              # Banco de las 30 preguntas de evaluación
├── resultados_evaluacion.json  # Registro de notas y exámenes entregados
├── INICIAR_EVALUACION.bat      # Lanzador en 1 clic para entornos Windows
├── requirements.txt            # Manifiesto para despliegue en la nube
├── render.yaml                 # Configuración de infraestructura como código (Render)
├── Juego_Evaluacion_SQL.html   # Versión autocontenida para ejecución offline
└── README.md                   # Documentación general del proyecto
```

---

## 👤 Autor y Docente

* **Docente:** Mae. Carlos Alfredo Hernández Quintanilla  
* **Asignatura:** Auditoría de Sistemas Informáticos
