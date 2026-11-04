Auditoría de Sistemas Informáticos · Protección de Activos de Información 

**A U D I T O R Í A D E S I S T E M A S I N F O R M Á T I C O S** 

# **Guía de Investigación Grupal** 

Protección de Activos de Información 

|**Datos generales**||
|---|---|
|**Asignatura**|Auditoría de Sistemas Informáticos|
|**Tema principal**|Protección de activos de información|
|**Subtema 1**|Controles ambientales|
|**Subtema 2**|Seguridad lógica en plataformas de bases de datos (práctica con<br>MySQL)|
|**Modalidad**|Investigación grupal|
|**Docente**|Mae. Carlos Alfredo Hernández Quintanilla.|
|**Grupo / Integrantes**||
|**Fecha de asignación**|22/10/2026|
|**Fecha de entrega**|29/10/2026|



# **1. Presentación** 

Los activos de información (datos, sistemas, aplicaciones, equipos e instalaciones que los soportan) son uno de los recursos más valiosos de cualquier organización. El auditor de sistemas debe ser capaz de evaluar si dichos activos están protegidos tanto contra amenazas **físicas y ambientales** (fuego, inundaciones, fallas eléctricas, temperatura inadecuada, acceso no autorizado a las instalaciones) como contra amenazas **lógicas** (accesos indebidos, privilegios excesivos, contraseñas débiles, falta de registros de auditoría, ausencia de respaldos). 

Esta guía establece las indicaciones para desarrollar una investigación sobre dos subtemas complementarios: los **controles ambientales** que protegen el entorno donde operan los sistemas, y la **seguridad lógica en plataformas de bases de datos** , donde reside la información crítica del negocio. El segundo subtema incluye una práctica introductoria en MySQL que permitirá observar, en un entorno controlado, la aplicación de controles básicos de seguridad y su verificación desde la óptica de un auditor. 

Página 1 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

# **2. Objetivos** 

# **Objetivo general** 

Analizar los controles ambientales y los controles de seguridad lógica en bases de datos como mecanismos de protección de los activos de información, aplicando criterios propios de la auditoría de sistemas. 

# **Objetivos específicos** 

- Identificar las principales amenazas ambientales sobre un centro de procesamiento de datos y los controles preventivos, detectivos y correctivos asociados. 

- Explicar los principios de seguridad lógica aplicables a plataformas de bases de datos: autenticación, autorización, mínimo privilegio, cifrado, registro de eventos y respaldo. 

- Investigar, probar y analizar en MySQL ejercicios básicos de gestión de usuarios, privilegios y configuraciones de seguridad, documentando la evidencia obtenida. 

- Elaborar hallazgos de auditoría con estructura formal (condición, criterio, causa, efecto y recomendación) a partir de la investigación y la práctica. 

- Desarrollar habilidades de trabajo colaborativo, citación de fuentes y comunicación técnica. 

# **3. Organización del grupo** 

Los grupos ya están conformados. Cada grupo debe distribuir las responsabilidades al inicio de la actividad y registrarlas en el informe. Si el grupo tiene menos de cinco integrantes, se pueden combinar roles; si tiene más, se pueden asignar apoyos. 

|**Rol**|**Responsabilidad principal**|
|---|---|
|**Coordinador(a)**|Controla el avance según el cronograma, modera las discusiones<br>y verifica que se cumplan los entregables.|
|**Investigador(a)**<br>**del**<br>**subtema 1**|Lidera la búsqueda y el análisis de fuentes sobre controles<br>ambientales y completa la matriz de la sección 4.4.|
|**Investigador(a)**<br>**del**<br>**subtema 2**|Lidera la investigación sobre seguridad lógica en bases de datos<br>y la matriz de verificación de la sección 5.5.|
|**Responsable técnico(a) de**<br>**la práctica**|Coordina la realización de los ejercicios en MySQL, captura la<br>evidencia y resguarda el archivo de comandos.|
|**Redactor(a) y control de**<br>**fuentes**|Unifica el estilo del informe, revisa ortografía y verifica que toda<br>cita tenga su referencia en formato APA 7.|



**Nota:** aunque existan roles, todos los integrantes deben conocer y poder explicar la totalidad del trabajo. El docente podrá formular preguntas a cualquier miembro del grupo al revisar el trabajo. 

Página 2 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

# **4. Subtema 1: Controles ambientales** 

# **4.1 Qué se espera de la investigación** 

Los controles ambientales son las medidas que protegen las instalaciones y los equipos que alojan los sistemas de información frente a condiciones del entorno y a eventos físicos. La investigación debe explicar cada control, justificar su necesidad mediante el riesgo que mitiga y describir cómo un auditor puede comprobar su existencia y su funcionamiento. 

# **4.2 Ejes de investigación** 

Cada grupo debe desarrollar como mínimo los siguientes ejes. Se pueden agregar otros que el grupo considere pertinentes. 

|**Eje**||**Aspectos a investigar**|**Ejemplos de controles**|
|---|---|---|---|
|**Ubicación**<br>**construcción**<br>**centro de datos**|**y**<br>**del**|Selección del sitio, riesgos<br>geográficos<br>(sismos,<br>inundaciones), estructura, piso<br>falso, señalización.|Evitar sótanos y plantas bajas<br>expuestas, ausencia de rótulos que<br>identifiquen el sitio, evaluación de<br>riesgos previa.|
|**Prevención**<br>**control**<br>**incendios**|**y**<br>**de**|Detección, supresión, materiales,<br>rutas<br>de<br>evacuación<br>y<br>mantenimiento.|Detectores de humo, extintores,<br>sistemas de supresión con agentes<br>limpios, rociadores, simulacros.|
|**Suministro**<br>**eléctrico**||Continuidad y calidad de la<br>energía,<br>redundancia,<br>mantenimiento.|UPS, planta eléctrica, reguladores,<br>tableros identificados, puesta a<br>tierra.|
|**Climatización**<br>**humedad**|**y**|Temperatura, humedad relativa,<br>ventilación, pasillos fríos y<br>calientes.|Aire acondicionado de precisión,<br>sensores de temperatura y<br>humedad, alertas automáticas.|
|**Protección con**<br>**agua**<br>**inundaciones**|**tra**<br>**e**|Fuentes de filtración, drenajes,<br>tuberías cercanas.|Sensores de agua, drenajes, equipos<br>elevados<br>del<br>piso,<br>impermeabilización.|
|**Control de acc**<br>**físico**|**eso**|Quién puede ingresar y cómo se<br>registra.|Tarjetas de proximidad, biometría,<br>bitácoras,<br>cámaras<br>de<br>videovigilancia, acompañamiento<br>de visitantes.|
|**Cableado**<br>**comunicaciones**|**y**|Protección de cables de datos y<br>energía.|Canalización,<br>etiquetado,<br>separación entre cables de datos y<br>de potencia, protección contra<br>interferencias.|



Página 3 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

|**Eje**||**Aspectos a investigar**||**Ejemplos de controles**|
|---|---|---|---|---|
|**Monitoreo**|**y**|Supervisión<br>continua|y|Sistemas de monitoreo ambiental,|
|**mantenimiento**||mantenimiento preventivo.||contratos de mantenimiento,<br>registros de pruebas.|



# **4.3 Preguntas guía** 

1. ¿Qué amenazas ambientales y físicas son más relevantes para un centro de datos y por qué? 

2. ¿Cuál es la diferencia entre un control preventivo, uno detectivo y uno correctivo? Clasifique al menos un control de cada eje investigado. 

3. ¿Qué evidencia puede solicitar un auditor para comprobar que un control ambiental realmente funciona (registros de mantenimiento, bitácoras, pruebas, certificados)? 

4. ¿Qué estándares o marcos de referencia abordan la seguridad física y ambiental (por ejemplo, ISO/IEC 27001 y 27002, ANSI/TIA-942, NFPA 75, COBIT)? Resuma qué exige cada uno. 

5. ¿Cómo cambia la evaluación de estos controles si la organización usa un centro de datos propio, un proveedor de alojamiento (colocation) o servicios en la nube? 

6. Presente un caso real o documentado de una falla ambiental que afectó la continuidad de un servicio y analice qué control habría evitado o reducido el impacto. 

# **4.4 Matriz de análisis de controles ambientales** 

Cada grupo elaborará y completará esta matriz como si evaluara un centro de datos hipotético o uno real al que tenga acceso (por ejemplo, el laboratorio o el cuarto de servidores de la institución, con autorización del docente). Se sugieren las filas iniciales; el grupo debe agregar al menos cuatro controles más. 

|**Control**||**Riesgo**<br>**mitiga**|**que**|**Tipo**|**Evidencia**<br>**solicitar**|**a**|**Cumple**|**Observación**|
|---|---|---|---|---|---|---|---|---|
|Detectores<br>humo|de|Incendio<br>detectado<br>tiempo|no<br>a|Detectivo|Certificado<br>mantenimien<br>pruebas|de<br>to,|||
|Extintores<br>vigentes||Propagaci<br>del fuego|ón|Correctivo|Etiquetas<br>recarga,<br>inspección|de|||
|UPS<br>pruebas<br>periódicas|con|Apagón<br>pérdida<br>datos|y<br>de|Preventivo|Bitácora<br>pruebas,<br>autonomía|de|||



Página 4 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

|**Control**||**Riesgo**<br>**mitiga**|**que**|**Tipo**|**Evidencia**<br>**a**<br>**solicitar**|**Cumple**|**Observación**|
|---|---|---|---|---|---|---|---|
|Control<br>temperatura<br>humedad|de<br>y|Daño o<br>de equipo|falla<br>s|Preventivo<br>/ detectivo|Lecturas<br>de<br>sensores, alertas|||
|Registro<br>acceso<br>cuarto<br>servidores|de<br>al<br>de|Ingreso<br>autorizado|no<br>|Preventivo<br>/ detectivo|Bitácora, lista de<br>personas<br>autorizadas|||



_Cumple: Sí / No / Parcial / No aplica._ 

# **4.5 Entregable del subtema 1** 

- Desarrollo teórico de los ejes de investigación (extensión sugerida: 4 a 6 páginas). 

- Matriz de evaluación completada, con al menos nueve controles. 

- Conclusiones propias del grupo sobre la importancia de estos controles para la auditoría. 

# **5. Subtema 2: Seguridad lógica en plataformas de bases de datos** 

# **5.1 Qué se espera de la investigación** 

La seguridad lógica comprende los controles de software que restringen el acceso a los datos y a los sistemas que los gestionan. En una base de datos, estos controles deben garantizar la confidencialidad, la integridad y la disponibilidad de la información. La investigación debe presentar los conceptos fundamentales, relacionarlos con el trabajo del auditor y respaldarlos con la práctica en MySQL. 

# **5.2 Ejes de investigación** 

|**Eje**||**Aspectos a investigar**|
|---|---|---|
|**Autenticación**||Cuentas de usuario, contraseñas, políticas de complejidad, expiración<br>y bloqueo; cuentas por defecto y anónimas; autenticación multifactor<br>y centralizada.|
|**Autorización**|**y**|Privilegios globales, por base de datos, por tabla y por columna; roles;|
|**mínimo privilegio**||separación de funciones; revisión periódica de accesos.|



Página 5 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

|**Eje**|**Aspectos a investigar**|
|---|---|
|**Cifrado**|Cifrado en tránsito (TLS/SSL) y en reposo; manejo de llaves;<br>enmascaramiento de datos sensibles.|
|**Registro y auditoría**|Registros de errores, de consultas y de conexiones; auditoría de<br>acciones privilegiadas; conservación y protección de los registros.|
|**Respaldo**<br>**y**<br>**recuperación**|Tipos de respaldo, frecuencia, pruebas de restauración, resguardo<br>fuera del sitio.|
|**Configuración segura**<br>**(hardening)**|Eliminación de componentes y cuentas innecesarias, restricción de<br>conexiones remotas, puertos, actualizaciones y parches, guías de<br>referencia como los CIS Benchmarks.|
|**Amenazas comunes**|Inyección SQL, escalamiento de privilegios, fuerza bruta, exposición<br>de bases de datos a internet, filtración de respaldos.|



# **5.3 Preguntas guía** 

1. ¿Qué significa el principio de mínimo privilegio y cómo se implementa en un gestor de bases de datos relacional? 

2. ¿Qué diferencia hay entre autenticación y autorización? Dé un ejemplo concreto en MySQL. 

3. ¿Qué riesgos implica que la cuenta administradora (root) pueda conectarse desde cualquier equipo de la red? 

4. ¿Qué registros de MySQL puede revisar un auditor y qué limitaciones tienen frente a una solución de auditoría especializada? 

5. ¿Cómo se comprueba que los respaldos son confiables? ¿Por qué un respaldo que nunca se ha restaurado no ofrece garantía? 

6. ¿Qué controles de la norma ISO/IEC 27002 o del marco COBIT se relacionan con la gestión de accesos y la protección de bases de datos? 

7. Compare brevemente las funciones de seguridad de MySQL con las de otro gestor (por ejemplo, PostgreSQL, SQL Server u Oracle). 

# **5.4 Ejercicios de investigación práctica en MySQL.** 

# **Propósito** 

Esta parte del trabajo no entrega comandos ni procedimientos resueltos: cada grupo debe **investigar** en la documentación oficial y en fuentes confiables cómo se realiza cada ejercicio, **probarlo** en un entorno de laboratorio propio y **analizarlo** desde la óptica de un auditor (qué riesgo mitiga el control, cómo se verifica y qué evidencia deja). Los ejercicios son de nivel introductorio y están pensados para trabajar con comandos básicos de seguridad. 

Página 6 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

# **Requisitos del entorno** 

- MySQL Server 8.0 o superior, instalado en una computadora personal, en una máquina virtual o en un contenedor (el grupo decide y justifica su elección). 

- Cliente de línea de comandos o MySQL Workbench. 

- Acceso a una cuenta administradora del entorno de práctica. 

- Herramienta de captura de pantalla para documentar la evidencia. 

# **Ejercicios a investigar, probar y analizar** 

|**N.º**|**Ejercicio**|**Qué deben investigar**|**Qué deben probar y analizar**|
|---|---|---|---|
|1|Conexión<br>y<br>reconocimiento<br>del entorno|Formas de conectarse a MySQL,<br>cómo obtener la versión del<br>servidor, el usuario actual y las<br>bases existentes; por qué la<br>versión es relevante para un<br>auditor.|Conectarse al servidor y<br>documentar versión, usuario y<br>bases de datos encontradas.|
|2|Revisión<br>de<br>cuentas<br>existentes|Dónde almacena MySQL las<br>cuentas y qué atributos tienen<br>(host, bloqueo, expiración);<br>riesgos de cuentas anónimas, sin<br>contraseña o administradoras<br>accesibles desde cualquier<br>equipo.|Listar las cuentas del servidor,<br>identificar posibles riesgos y<br>justificar cada uno.|
|3|Base de datos de<br>práctica|Cómo crear una base de datos y<br>tablas; qué datos ficticios<br>sensibles usar (por ejemplo,<br>empleados y salarios).|Crear una base con al menos dos<br>tablas y datos ficticios que<br>servirán para el resto de los<br>ejercicios.|
|4|Creación<br>de<br>usuarios|Cómo se crean cuentas con<br>contraseña; qué significa el host<br>asociado a una cuenta y qué<br>implica permitir conexiones<br>desde cualquier equipo.|Crear al menos dos cuentas con<br>funciones distintas (por ejemplo,<br>auditor y operador) y analizar el<br>efecto de restringir el origen de la<br>conexión.|
|5|Privilegios<br>mínimos|Tipos de privilegios y sus niveles<br>(global, base de datos, tabla,<br>columna); cómo consultar los<br>privilegios de una cuenta;<br>principio de mínimo privilegio.|Asignar a cada cuenta solo lo<br>necesario, iniciar sesión con cada<br>una,<br>intentar<br>operaciones<br>permitidas y no permitidas, y<br>analizar los mensajes de error.|



Página 7 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

|**N.º**|**Ejercicio**||**Qué deben investigar**|**Qué deben probar y analizar**|
|---|---|---|---|---|
|6|Uso de roles||Qué son los roles en MySQL 8,<br>cómo se crean, asignan y activan;<br>ventajas para la administración y<br>el control de accesos.|Crear un rol de consulta,<br>asignarlo a una cuenta y<br>comprobar los privilegios<br>efectivos.|
|7|Revocación<br>privilegios|de|Cómo se retiran privilegios y por<br>qué la revisión periódica de<br>accesos es un control de<br>auditoría.|Retirar un privilegio a una cuenta<br>y verificar que el cambio se<br>aplicó.|
|8|Contraseñas,<br>expiración<br>bloqueo|<br>y|Políticas<br>de<br>complejidad,<br>expiración y bloqueo por intentos<br>fallidos; requisitos de versión;<br>qué exigen ISO/IEC 27002 o<br>COBIT sobre gestión de<br>contraseñas.|Configurar una política, probar<br>con una contraseña débil y con<br>intentos de acceso fallidos, y<br>documentar el comportamiento<br>del servidor.|
|9|Cifrado de<br>conexión<br>tránsito)|la<br>(en|Cómo soporta MySQL las<br>conexiones cifradas, cómo<br>comprobar si una sesión está<br>cifrada y cómo exigirlo por<br>cuenta.|Verificar el estado del cifrado,<br>exigirlo a una cuenta y analizar el<br>efecto sobre las conexiones.|
|10|Registros<br>auditoría|para|Tipos de registro de MySQL<br>(errores, consultas, otros), dónde<br>se almacenan, sus riesgos y<br>limitaciones; alternativas de<br>auditoría especializada.|Activar temporalmente el registro<br>de consultas en el laboratorio,<br>ejecutar acciones con distintas<br>cuentas, revisar lo que queda<br>registrado y desactivarlo.|
|11|Respaldo<br>restauración|y|Herramientas de respaldo lógico<br>y físico de MySQL, frecuencia,<br>resguardo y pruebas de<br>restauración.|Generar un respaldo de la base de<br>práctica, restaurarlo en otra base<br>y comprobar que la información<br>es íntegra.|
|12|Limpieza<br>entorno|del|Cómo eliminar cuentas, roles y<br>bases de datos; por qué un auditor<br>verifica que no queden cuentas<br>residuales.|Dejar el entorno de laboratorio<br>limpio y documentar lo<br>eliminado.|



Página 8 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

# **Cómo documentar cada ejercicio** 

Para cada uno de los doce ejercicios, el informe debe incluir una ficha breve con los siguientes puntos: 

- **Procedimiento:** qué se hizo, con los comandos o pasos utilizados por el grupo y su fuente. 

- **Evidencia:** captura de pantalla legible del resultado, incluidos los mensajes de error cuando existan. 

- **Análisis:** qué riesgo mitiga el control, cómo lo verificaría un auditor y qué limitaciones se observaron. 

- **Observaciones:** diferencias entre lo esperado y lo obtenido. 

Además, el grupo conservará un archivo de texto con los comandos ejecutados, en el orden en que los aplicó, como anexo. 

# **5.5 Entregable del subtema 2** 

- Desarrollo teórico de los ejes de investigación (extensión sugerida: 4 a 6 páginas). 

- Anexo con la evidencia de la práctica y el archivo de comandos. 

- Análisis de resultados: qué controles funcionaron, cuáles fallaron y qué riesgos quedarían en un ambiente real. 

# **6. Formato de hallazgos de auditoría** 

A partir de la investigación y de la práctica, cada grupo redactará un mínimo de **cuatro hallazgos** (dos por subtema). Cada hallazgo debe contar con los cinco atributos clásicos: 

|**Atributo**|**Descripción**|**Ejemplo (subtema 2)**|
|---|---|---|
|**Condición**|Qué se encontró (la situación<br>actual).|La cuenta administradora acepta<br>conexiones desde cualquier equipo de la<br>red.|
|**Criterio**|Qué debería ocurrir (norma,<br>política, buena práctica).|La política de seguridad y las buenas<br>prácticas indican restringir el acceso<br>administrativo a equipos autorizados.|
|**Causa**|Por qué ocurrió la desviación.|No se aplicaron configuraciones de<br>endurecimiento tras la instalación.|
|**Efecto**|Riesgo o impacto resultante.|Mayor probabilidad de acceso no<br>autorizado con control total de los datos.|
|**Recomendació**<br>**n**|Acción correctiva propuesta.|Restringir la cuenta a localhost y crear<br>cuentas nominales con privilegios<br>limitados.|



Página 9 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

Se recomienda clasificar cada hallazgo por nivel de riesgo (alto, medio o bajo) y justificar la clasificación. 

# **7. Estructura del informe final** 

1. **Portada:** institución, asignatura, título, docente, integrantes con sus carnés y fecha. 

2. **Índice.** 

3. **Introducción:** contexto, importancia del tema y descripción del contenido del informe. 

4. **Objetivos** del trabajo. 

5. **Desarrollo del subtema 1:** controles ambientales (incluye la matriz de la sección 4.4). 

6. **Desarrollo del subtema 2:** seguridad lógica en bases de datos (incluye la práctica y la matriz de la sección 5.5). 

7. **Hallazgos y recomendaciones** en el formato de la sección 6. 

8. **Conclusiones:** propias del grupo, vinculadas con los objetivos. 

9. **Referencias:** formato APA 7.ª edición. 

10. **Anexos:** capturas de pantalla, archivo de comandos y material de apoyo. 

# **8. Formato y condiciones de entrega** 

- Extensión sugerida del cuerpo del informe: entre 12 y 18 páginas, sin contar portada, índice, referencias ni anexos. 

- Letra Arial o Times New Roman a 12 puntos, interlineado de 1.5, márgenes de 2.5 cm y texto justificado. 

- Citas y referencias en formato APA 7.ª edición; mínimo de 8 fuentes confiables (normas, libros, artículos académicos, documentación oficial del fabricante). 

- No se aceptan como fuente principal blogs sin autoría, foros ni resúmenes sin respaldo. 

- Entrega en formato PDF. 

- Todas las capturas deben ser de la práctica realizada por el propio grupo. 

# **9. Criterios de evaluación** 

|**Criterio**|**Descripción**|**Puntos**|
|---|---|---|
|Subtema 1: controles<br>ambientales|Profundidad, claridad y vinculación con la auditoría;<br>matriz completa y coherente.|20|
|Subtema 2: marco teórico|Dominio de los conceptos de seguridad lógica y uso<br>adecuado de estándares.|20|



Página 10 de 11 

Auditoría de Sistemas Informáticos · Protección de Activos de Información 

|**Criterio**||**Descripción**|**Puntos**|
|---|---|---|---|
|Práctica en MySQL||Ejecución correcta, evidencias completas y matriz de<br>verificación.|20|
|Hallazgos<br>recomendaciones|y|Estructura formal, pertinencia, razonamiento del<br>riesgo.|15|
|Fuentes y citación||Calidad, cantidad y correcto uso del formato APA.|10|
|Redacción y presentación||Ortografía, coherencia, formato y orden del informe.|5|
|Trabajo en equipo||Aporte equitativo de los integrantes, coordinación del<br>grupo y dominio del contenido al responder<br>preguntas.|10|
|Total|||100|



# **10. Fuentes sugeridas para iniciar** 

- ISO/IEC 27001 e ISO/IEC 27002: requisitos y controles de seguridad de la información (secciones sobre seguridad física y ambiental y control de acceso). 

- ISACA: marco COBIT y material de preparación de la certificación CISA (dominios sobre protección de activos de información). 

- NIST SP 800-53: controles de seguridad y privacidad, familias de protección física y ambiental y de control de acceso. 

- ANSI/TIA-942 y NFPA 75: infraestructura de centros de datos y protección contra incendios de equipos de tecnología de la información. 

- Documentación oficial de MySQL: capítulo de seguridad del manual de referencia (cuentas de usuario, control de acceso, roles, conexiones cifradas, registros). 

- CIS Benchmarks para MySQL: guía de configuración segura publicada por el Center for Internet Security. 

- Libros de texto de auditoría de sistemas y seguridad informática disponibles en la biblioteca de la institución. 

Página 11 de 11 

