# -*- coding: utf-8 -*-
"""
Servidor de Evaluación Interactiva para Alumnos y Docente
Diseño: Neumórfico / Soft UI (basado en referencia.jpg)
Efectos: Confeti verde para aciertos + Luffy cómplice One Piece para fallos
Seguridad: Bloqueo anti-reintentos por carné + Auto-guardado y reanudación ante F5/recargas
Asignatura: Auditoría de Sistemas Informáticos
Base de Datos: MySQL 8.0 - Seguridad Lógica
"""

import sys
import os
import json
import socket
import csv
import io
from datetime import datetime
try:
    from http.server import ThreadingHTTPServer as ServerClass
except ImportError:
    from http.server import HTTPServer as ServerClass
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORT", 8000))
PIN_DOCENTE = "Carlos.26"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREGUNTAS_FILE = os.path.join(BASE_DIR, "preguntas.json")
RESULTADOS_FILE = os.path.join(BASE_DIR, "resultados_evaluacion.json")

# Asegurar archivo de resultados
if not os.path.exists(RESULTADOS_FILE):
    with open(RESULTADOS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# Cargar preguntas
if os.path.exists(PREGUNTAS_FILE):
    with open(PREGUNTAS_FILE, "r", encoding="utf-8") as f:
        PREGUNTAS_DATA = json.load(f)
else:
    PREGUNTAS_DATA = []

# Tripulación Sombrero de Paja para retroalimentación cómica
MUGIWARA_CREW_DATA = [
  {
    "id": "luffy",
    "name": "Monkey D. Luffy",
    "role": "Capitán",
    "icon": "👒",
    "sound": "luffy",
    "color": "#dc2626",
    "bgLight": "#fef2f2",
    "border": "#f87171",
    "title": "¡SHISHISHI! ¡FALLASTE LA CONSULTA, NAKAMA!",
    "quotes": [
      "¡SHISHISHI! ¡Ni activando el Gear 5 salvaste esa consulta, nakama!",
      "¡¿NANIIIII?! ¡Tengo tanta hambre de carne que hasta yo sé que esa no era la respuesta!",
      "¡Gomu Gomu no... ERROR FATAL! ¡Esa sintaxis mandó la base de datos al fondo del océano!",
      "¡Shishishi! ¡Te comiste la Fruta del Error-Error no Mi! ¡No sabes nadar ni configurar un GRANT!",
      "¡¿Buggy el Payaso te sopló esa respuesta?! ¡Esa opción no existe ni en el Grand Line!",
      "¡Chopper, trae carne y el botiquín urgente! ¡Acaban de romper la integridad referencial!",
      "¡Shishishi! ¡Tranquilo nakama, hasta el futuro Rey de los Piratas tropieza a veces!",
      "¡Gishishi! ¡Esa consulta fue directo a Impel Down Nivel 6 sin derecho a fianza!",
      "¡Oye! ¡Si no estás seguro de la respuesta no inventes como Usopp! ¡Lee bien la bitácora!",
      "¡Shishishi! ¡Ese host '%' que pusiste está más regalado que un banquete en Arabasta!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <ellipse cx=\"60\" cy=\"38\" rx=\"55\" ry=\"16\" fill=\"#eab308\" stroke=\"#ca8a04\" stroke-width=\"3\"/>\n  <path d=\"M30,36 C30,12 90,12 90,36 Z\" fill=\"#eab308\" stroke=\"#ca8a04\" stroke-width=\"3\"/>\n  <path d=\"M30,34 C45,39 75,39 90,34 L90,27 C75,32 45,32 30,27 Z\" fill=\"#dc2626\"/>\n  <path d=\"M25,44 Q35,60 22,70 Q40,65 38,78 Q50,60 52,48\" fill=\"#18181b\"/>\n  <path d=\"M95,44 Q85,60 98,70 Q80,65 82,78 Q70,60 68,48\" fill=\"#18181b\"/>\n  <ellipse cx=\"60\" cy=\"66\" rx=\"34\" ry=\"32\" fill=\"#fed7aa\"/>\n  <path d=\"M70,68 L78,72 M72,68 L74,72 M76,69 L77,73\" stroke=\"#991b1b\" stroke-width=\"2\" stroke-linecap=\"round\"/>\n  <ellipse cx=\"46\" cy=\"56\" rx=\"7.5\" ry=\"9\" fill=\"#ffffff\" stroke=\"#18181b\" stroke-width=\"2.5\"/>\n  <ellipse cx=\"74\" cy=\"56\" rx=\"7.5\" ry=\"9\" fill=\"#ffffff\" stroke=\"#18181b\" stroke-width=\"2.5\"/>\n  <circle cx=\"46\" cy=\"56\" r=\"3.5\" fill=\"#18181b\"/>\n  <circle cx=\"74\" cy=\"56\" r=\"3.5\" fill=\"#18181b\"/>\n  <circle cx=\"48\" cy=\"54\" r=\"1.5\" fill=\"#ffffff\"/>\n  <circle cx=\"76\" cy=\"54\" r=\"1.5\" fill=\"#ffffff\"/>\n  <ellipse cx=\"34\" cy=\"67\" rx=\"5\" ry=\"3\" fill=\"#fca5a5\" opacity=\"0.8\"/>\n  <ellipse cx=\"86\" cy=\"67\" rx=\"5\" ry=\"3\" fill=\"#fca5a5\" opacity=\"0.8\"/>\n  <path d=\"M36,73 Q60,104 84,73 Z\" fill=\"#991b1b\" stroke=\"#18181b\" stroke-width=\"3\"/>\n  <path d=\"M39,75 Q60,94 81,75 Z\" fill=\"#ffffff\"/>\n  <line x1=\"60\" y1=\"75\" x2=\"60\" y2=\"90\" stroke=\"#d1d5db\" stroke-width=\"2\"/>\n  <line x1=\"50\" y1=\"75\" x2=\"50\" y2=\"86\" stroke=\"#d1d5db\" stroke-width=\"1.5\"/>\n  <line x1=\"70\" y1=\"75\" x2=\"70\" y2=\"86\" stroke=\"#d1d5db\" stroke-width=\"1.5\"/>\n</svg>"
  },
  {
    "id": "zoro",
    "name": "Roronoa Zoro",
    "role": "Espadachín",
    "icon": "⚔️",
    "sound": "zoro",
    "color": "#059669",
    "bgLight": "#ecfdf5",
    "border": "#34d399",
    "title": "¡TE PERDISTE DE TABLA, NAKAMA!",
    "quotes": [
      "¡Oye! ¡Hasta yo con mi pésimo sentido de orientación sé que por ahí no iba la consulta!",
      "¡Santoryu: Corte de los Tres Errores! ¡Te perdiste peor que yo buscando el baño en Wano!",
      "¿Seguro que leíste la guía de auditoría? Te fuiste en dirección exactamente contraria al servidor...",
      "Un verdadero espadachín nunca falla una estocada... ¡pero tú le diste DELETE a todo sin WHERE!",
      "¡Tch! ¡Esa respuesta no corta ni un archivo temporal! ¡Desenvaina mejor la sintaxis!",
      "¿Quién puso esa opción ahí? Juraría que el camino a la clave foránea estaba a la derecha...",
      "Si no sabes la respuesta, ¡entrena mil flexiones antes de volver a tocar la consola!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M26,52 Q24,18 60,18 Q96,18 94,52 Z\" fill=\"#16a34a\"/>\n  <path d=\"M30,35 Q60,25 90,35 Q85,15 60,15 Q35,15 30,35 Z\" fill=\"#15803d\"/>\n  <ellipse cx=\"60\" cy=\"66\" rx=\"33\" ry=\"31\" fill=\"#fed7aa\"/>\n  <path d=\"M28,45 Q60,38 92,45 L93,52 Q60,45 27,52 Z\" fill=\"#14532d\"/>\n  <path d=\"M38,48 Q48,43 54,49\" stroke=\"#0f172a\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n  <path d=\"M66,49 Q72,43 82,48\" stroke=\"#0f172a\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n  <ellipse cx=\"46\" cy=\"56\" rx=\"6\" ry=\"6\" fill=\"#ffffff\" stroke=\"#0f172a\" stroke-width=\"2\"/>\n  <circle cx=\"46\" cy=\"56\" r=\"3\" fill=\"#0f172a\"/>\n  <circle cx=\"47\" cy=\"55\" r=\"1.2\" fill=\"#ffffff\"/>\n  <path d=\"M74,48 L74,65\" stroke=\"#7f1d1d\" stroke-width=\"2.5\" stroke-linecap=\"round\"/>\n  <path d=\"M70,57 L78,57\" stroke=\"#0f172a\" stroke-width=\"2.5\" stroke-linecap=\"round\"/>\n  <circle cx=\"28\" cy=\"68\" r=\"2.5\" fill=\"#eab308\"/>\n  <circle cx=\"28\" cy=\"73\" r=\"2.5\" fill=\"#eab308\"/>\n  <circle cx=\"28\" cy=\"78\" r=\"2.5\" fill=\"#eab308\"/>\n  <path d=\"M45,77 Q55,73 75,76\" stroke=\"#0f172a\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n  <path d=\"M68,76 L75,72 L73,79 Z\" fill=\"#ffffff\" stroke=\"#0f172a\" stroke-width=\"1.5\"/>\n</svg>"
  },
  {
    "id": "nami",
    "name": "Nami",
    "role": "Navegante",
    "icon": "🍊",
    "sound": "nami",
    "color": "#ea580c",
    "bgLight": "#fff7ed",
    "border": "#fb923c",
    "title": "¡¿PERO QUÉ HICISTE?! ¡NOS COSTARÁ MILLONES!",
    "quotes": [
      "¡¿Pero qué hiciste?! ¡Restaurar ese desastre nos va a costar 100 millones de Berries! ¡Y te cobraré un 200% de interés!",
      "¡Clima-Tact: Tormenta de Errores! Con esa respuesta no cruzamos ni el Reverse Mountain.",
      "¡Idiota! ¡Si cobrara un Berry por cada consulta mal redactada, ya le habría comprado la isla a Arlong!",
      "¡Mira el mapa de privilegios! ¡Ese usuario tenía permisos de root y ni cuenta te diste!",
      "¡¿Acaso no consultaste el Log Pose de la auditoría?! ¡Caíste directito en la trampa del examen!",
      "¡Un buen navegante lee el clima y un buen auditor lee el log de errores! ¡Presta atención!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M22,60 Q18,22 60,20 Q102,22 98,60 Q96,95 86,95 Q90,70 82,50 Q60,35 38,50 Q30,70 34,95 Q24,95 22,60 Z\" fill=\"#ea580c\"/>\n  <ellipse cx=\"60\" cy=\"64\" rx=\"31\" ry=\"29\" fill=\"#ffedd5\"/>\n  <path d=\"M32,42 Q45,32 60,40 Q75,32 88,42\" fill=\"#f97316\"/>\n  <path d=\"M38,50 Q46,45 54,49\" stroke=\"#9a3412\" stroke-width=\"2.5\" fill=\"none\"/>\n  <path d=\"M66,49 Q74,45 82,50\" stroke=\"#9a3412\" stroke-width=\"2.5\" fill=\"none\"/>\n  <ellipse cx=\"46\" cy=\"57\" rx=\"6.5\" ry=\"8\" fill=\"#78350f\"/>\n  <circle cx=\"47\" cy=\"55\" r=\"2\" fill=\"#ffffff\"/>\n  <ellipse cx=\"74\" cy=\"57\" rx=\"6.5\" ry=\"8\" fill=\"#78350f\"/>\n  <circle cx=\"75\" cy=\"55\" r=\"2\" fill=\"#ffffff\"/>\n  <circle cx=\"36\" cy=\"66\" r=\"5\" fill=\"#fca5a5\" opacity=\"0.7\"/>\n  <circle cx=\"84\" cy=\"66\" r=\"5\" fill=\"#fca5a5\" opacity=\"0.7\"/>\n  <path d=\"M46,74 Q60,86 74,74\" stroke=\"#9a3412\" stroke-width=\"2.5\" fill=\"#dc2626\"/>\n  <circle cx=\"28\" cy=\"30\" r=\"11\" fill=\"#f97316\"/>\n  <circle cx=\"28\" cy=\"28\" r=\"9\" fill=\"#fbbf24\"/>\n  <path d=\"M28,19 Q33,14 36,17\" stroke=\"#15803d\" stroke-width=\"2\" fill=\"none\"/>\n</svg>"
  },
  {
    "id": "usopp",
    "name": "God Usopp",
    "role": "Francotirador",
    "icon": "🎯",
    "sound": "usopp",
    "color": "#d97706",
    "bgLight": "#fffbeb",
    "border": "#fcd34d",
    "title": "¡AYUDAAAA! ¡ERROR NIVEL APOCALIPSIS!",
    "quotes": [
      "¡AYUDAAAA! ¡Me dio la legendaria 'Enfermedad de No Puedo Responder Preguntas de MySQL'!",
      "¡Por los 8,000 hombres a mi mando! ¡Hasta con los ojos cerrados mi resortera apunta mejor a la clave primaria!",
      "¡Hissatsu: Pachinko de Sintaxis Inválida! ¡Esa respuesta cayó a tres islas de distancia de la correcta!",
      "¡Tranquilo nakama! ¡Le diré al profesor que fue un ciberataque de la Marina y que yo nos salvé a todos!",
      "¡Sogeking! ¡En la Isla de los Francotiradores el 100% de los estudiantes se sabían esta pregunta!",
      "¡Waaaaah! ¡Si el docente revisa ese log de transacciones estamos perdidos!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <ellipse cx=\"60\" cy=\"40\" rx=\"38\" ry=\"24\" fill=\"#451a03\"/>\n  <circle cx=\"30\" cy=\"50\" r=\"14\" fill=\"#451a03\"/>\n  <circle cx=\"90\" cy=\"50\" r=\"14\" fill=\"#451a03\"/>\n  <ellipse cx=\"60\" cy=\"65\" rx=\"31\" ry=\"29\" fill=\"#fed7aa\"/>\n  <rect x=\"36\" y=\"32\" width=\"48\" height=\"12\" rx=\"4\" fill=\"#78350f\"/>\n  <circle cx=\"46\" cy=\"38\" r=\"6\" fill=\"#fbbf24\" stroke=\"#d97706\" stroke-width=\"2\"/>\n  <circle cx=\"74\" cy=\"38\" r=\"6\" fill=\"#fbbf24\" stroke=\"#d97706\" stroke-width=\"2\"/>\n  <ellipse cx=\"46\" cy=\"56\" rx=\"7\" ry=\"8\" fill=\"#ffffff\" stroke=\"#18181b\" stroke-width=\"2\"/>\n  <ellipse cx=\"74\" cy=\"56\" rx=\"7\" ry=\"8\" fill=\"#ffffff\" stroke=\"#18181b\" stroke-width=\"2\"/>\n  <circle cx=\"46\" cy=\"56\" r=\"3\" fill=\"#18181b\"/>\n  <circle cx=\"74\" cy=\"56\" r=\"3\" fill=\"#18181b\"/>\n  <path d=\"M58,58 L92,62 A6,6 0 0,1 92,72 L58,70 Z\" fill=\"#fdba74\" stroke=\"#ea580c\" stroke-width=\"2\"/>\n  <ellipse cx=\"60\" cy=\"80\" rx=\"14\" ry=\"7\" fill=\"#991b1b\" stroke=\"#18181b\" stroke-width=\"2\"/>\n  <path d=\"M50,77 Q60,82 70,77\" fill=\"#ffffff\"/>\n</svg>"
  },
  {
    "id": "sanji",
    "name": "Sanji",
    "role": "Cocinero",
    "icon": "🍳",
    "sound": "sanji",
    "color": "#2563eb",
    "bgLight": "#eff6ff",
    "border": "#60a5fa",
    "title": "¡ESA CONSULTA ESTÁ COMPLETAMENTE CRUDA!",
    "quotes": [
      "¡Maldita sea! ¡Serviste esa consulta tan cruda que todavía se mueve y hace DROP DATABASE en producción!",
      "¡Diable Jamble: Flambage de Examen! ¡Ese fallo quemó el CPU del servidor! ¡Ni en el Baratie servimos semejante horror!",
      "Un verdadero cocinero jamás desperdicia comida... ¡y un auditor jamás regala puntos con errores de novato!",
      "¡Oye, cabeza de marimo! Digo... ¡estudiante! ¡Fíjate bien en la sintaxis antes de mandarla a la parrilla!",
      "¡Si una señorita me pidiera auditar esa base de datos, jamás cometería semejante atrocidad!",
      "Cocinar requiere paciencia y precisión; la seguridad lógica también. ¡Vuelve a pensarlo bien!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M25,50 Q22,18 60,18 Q98,18 95,50 Q85,75 75,70 Q60,40 35,65 Z\" fill=\"#facc15\"/>\n  <ellipse cx=\"60\" cy=\"65\" rx=\"31\" ry=\"29\" fill=\"#ffedd5\"/>\n  <path d=\"M30,35 Q60,25 90,45 Q70,75 55,75 Q40,40 30,35 Z\" fill=\"#eab308\"/>\n  <path d=\"M68,48 Q76,44 82,48 Q85,46 87,49\" stroke=\"#854d0e\" stroke-width=\"2.5\" fill=\"none\" stroke-linecap=\"round\"/>\n  <ellipse cx=\"74\" cy=\"56\" rx=\"6\" ry=\"6\" fill=\"#0284c7\"/>\n  <circle cx=\"75\" cy=\"55\" r=\"2\" fill=\"#ffffff\"/>\n  <path d=\"M52,73 Q60,78 72,74\" stroke=\"#854d0e\" stroke-width=\"2.5\" fill=\"none\" stroke-linecap=\"round\"/>\n  <line x1=\"70\" y1=\"74\" x2=\"88\" y2=\"79\" stroke=\"#ffffff\" stroke-width=\"3.5\" stroke-linecap=\"round\"/>\n  <circle cx=\"89\" cy=\"79\" r=\"2\" fill=\"#ef4444\"/>\n  <path d=\"M90,77 Q94,70 91,65 Q95,60 93,55\" stroke=\"#94a3b8\" stroke-width=\"1.5\" fill=\"none\" opacity=\"0.7\"/>\n</svg>"
  },
  {
    "id": "chopper",
    "name": "Tony Tony Chopper",
    "role": "Médico",
    "icon": "🩺",
    "sound": "chopper",
    "color": "#ec4899",
    "bgLight": "#fdf2f8",
    "border": "#f472b6",
    "title": "¡MÉDICO RÁPIDO! ¡SE DESMAYÓ LA BASE DE DATOS!",
    "quotes": [
      "¡MÉDICO! ¡UN MÉDICO RÁPIDO! ... ¡Ah, si el médico soy yo! ¡Pero esa respuesta le dio un paro cardíaco a la base de datos!",
      "¡Rumble Ball: Error Point! ¡La integridad de las tablas está en estado sumamente crítico!",
      "¡Que me digas que fallaste la respuesta no me alegra para nada, bastardo con suerte! *(baila feliz de los nervios)*",
      "¡Te receto 500 mg de documentación oficial de MySQL 8.0 y reposo absoluto antes de tocar la terminal!",
      "¡Waaaah! ¡El pulso de la transacción cayó a cero! ¡Traigan el desfibrilador de respaldos mysqldump!",
      "¡Kureha me regañará si dejo que un alumno cometa semejante equivocación en los roles!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M24,34 Q14,24 16,14 Q22,14 26,22 Q32,12 36,18 Q32,28 32,34 Z\" fill=\"#78350f\"/>\n  <path d=\"M96,34 Q106,24 104,14 Q98,14 94,22 Q88,12 84,18 Q88,28 88,34 Z\" fill=\"#78350f\"/>\n  <ellipse cx=\"60\" cy=\"38\" rx=\"38\" ry=\"26\" fill=\"#ec4899\"/>\n  <ellipse cx=\"60\" cy=\"48\" rx=\"42\" ry=\"10\" fill=\"#db2777\"/>\n  <rect x=\"56\" y=\"24\" width=\"8\" height=\"22\" rx=\"2\" fill=\"#ffffff\"/>\n  <rect x=\"49\" y=\"31\" width=\"22\" height=\"8\" rx=\"2\" fill=\"#ffffff\"/>\n  <ellipse cx=\"60\" cy=\"74\" rx=\"28\" ry=\"24\" fill=\"#b45309\"/>\n  <ellipse cx=\"60\" cy=\"79\" rx=\"18\" ry=\"14\" fill=\"#fef3c7\"/>\n  <ellipse cx=\"46\" cy=\"68\" rx=\"6\" ry=\"8\" fill=\"#1e1b4b\"/>\n  <ellipse cx=\"74\" cy=\"68\" rx=\"6\" ry=\"8\" fill=\"#1e1b4b\"/>\n  <circle cx=\"48\" cy=\"66\" r=\"2.5\" fill=\"#ffffff\"/>\n  <circle cx=\"76\" cy=\"66\" r=\"2.5\" fill=\"#ffffff\"/>\n  <ellipse cx=\"60\" cy=\"75\" rx=\"5\" ry=\"3.5\" fill=\"#0284c7\"/>\n  <ellipse cx=\"36\" cy=\"76\" rx=\"5\" ry=\"3\" fill=\"#fda4af\"/>\n  <ellipse cx=\"84\" cy=\"76\" rx=\"5\" ry=\"3\" fill=\"#fda4af\"/>\n  <path d=\"M54,82 Q60,86 66,82\" stroke=\"#451a03\" stroke-width=\"2\" fill=\"none\"/>\n</svg>"
  },
  {
    "id": "robin",
    "name": "Nico Robin",
    "role": "Arqueóloga",
    "icon": "📚",
    "sound": "robin",
    "color": "#7c3aed",
    "bgLight": "#f5f3ff",
    "border": "#a78bfa",
    "title": "FUFUFU... TUS DATOS HAN QUEDADO EXTINTOS",
    "quotes": [
      "Fascinante... Si ejecutas esa consulta en producción, los registros quedarán tan extintos como los Poneglyphs de Ohara.",
      "Fufufu... Qué poético: un simple error de privilegios puede colapsar todo un imperio corporativo en segundos.",
      "Mil Fleurs: Gigantesco Error. Parece que alguien no leyó los registros históricos de auditoría.",
      "Fufufu... No te asustes, nakama. La muerte de tu calificación será rápida e indolora.",
      "Se dice que aquellos que no conocen las directivas de seguridad están condenados a ver sus tablas en cenizas...",
      "La verdad del siglo vacío de MySQL sigue oculta para quienes confunden GRANT con REVOKE."
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M26,55 Q20,20 60,18 Q100,20 94,55 Q92,90 85,92 Q78,50 60,35 Q42,50 35,92 Q28,90 26,55 Z\" fill=\"#18181b\"/>\n  <ellipse cx=\"60\" cy=\"65\" rx=\"30\" ry=\"28\" fill=\"#fed7aa\"/>\n  <path d=\"M38,32 Q60,26 82,32 L84,40 Q60,34 36,40 Z\" fill=\"#6d28d9\"/>\n  <ellipse cx=\"48\" cy=\"36\" rx=\"7\" ry=\"5\" fill=\"#1e1b4b\" stroke=\"#7c3aed\" stroke-width=\"1.5\"/>\n  <ellipse cx=\"72\" cy=\"36\" rx=\"7\" ry=\"5\" fill=\"#1e1b4b\" stroke=\"#7c3aed\" stroke-width=\"1.5\"/>\n  <path d=\"M40,51 Q48,47 54,51\" stroke=\"#312e81\" stroke-width=\"2.5\" fill=\"none\"/>\n  <path d=\"M66,51 Q72,47 80,51\" stroke=\"#312e81\" stroke-width=\"2.5\" fill=\"none\"/>\n  <ellipse cx=\"47\" cy=\"58\" rx=\"6\" ry=\"7\" fill=\"#0284c7\"/>\n  <circle cx=\"48\" cy=\"56\" r=\"2\" fill=\"#ffffff\"/>\n  <ellipse cx=\"73\" cy=\"58\" rx=\"6\" ry=\"7\" fill=\"#0284c7\"/>\n  <circle cx=\"74\" cy=\"56\" r=\"2\" fill=\"#ffffff\"/>\n  <path d=\"M52,74 Q60,78 68,74\" stroke=\"#831843\" stroke-width=\"2\" fill=\"none\"/>\n  <circle cx=\"28\" cy=\"72\" r=\"5\" fill=\"#f472b6\" opacity=\"0.8\"/>\n  <circle cx=\"92\" cy=\"72\" r=\"5\" fill=\"#f472b6\" opacity=\"0.8\"/>\n</svg>"
  },
  {
    "id": "franky",
    "name": "Franky",
    "role": "Carpintero Naval",
    "icon": "🦾",
    "sound": "franky",
    "color": "#06b6d4",
    "bgLight": "#ecfeff",
    "border": "#22d3ee",
    "title": "¡SUUUUUPER... MAL! ¡CERO ESTILO NAKAMA!",
    "quotes": [
      "¡SUUUUUPER... MAL! ¡Esa consulta no tiene nada de blindaje ni de carpintería naval de calidad!",
      "¡Coup de Vent! ¡El impacto de esa respuesta desarmó por completo el motor de almacenamiento del servidor!",
      "¡¿Quién construyó esa sentencia?! ¡No resiste ni la presión de una botella de cola vacía! ¡Hay que meterle blindaje SUUUUPER!",
      "¡Franky Shogun desaprobado! ¡Esa respuesta necesita reparaciones estructurales urgentes en el dique seco!",
      "¡Esta semana no me siento nada SUUUUPER con ese fallo! ¡Échale más cola al combustible mental!",
      "¡Un verdadero hombre defiende su barco y sus privilegios con cifrado TLS robusto!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M38,36 Q34,10 60,8 Q86,10 82,36 Z\" fill=\"#06b6d4\"/>\n  <path d=\"M42,28 Q60,18 78,28 L74,38 Q60,30 46,38 Z\" fill=\"#0891b2\"/>\n  <ellipse cx=\"60\" cy=\"68\" rx=\"33\" ry=\"30\" fill=\"#fed7aa\"/>\n  <path d=\"M32,46 L58,48 L56,58 L34,56 Z\" fill=\"#0f172a\"/>\n  <path d=\"M88,46 L62,48 L64,58 L86,56 Z\" fill=\"#0f172a\"/>\n  <line x1=\"58\" y1=\"50\" x2=\"62\" y2=\"50\" stroke=\"#0f172a\" stroke-width=\"3\"/>\n  <polygon points=\"56,60 64,60 60,70\" fill=\"#94a3b8\" stroke=\"#475569\" stroke-width=\"1.5\"/>\n  <path d=\"M40,78 Q60,94 80,78 Z\" fill=\"#991b1b\" stroke=\"#0f172a\" stroke-width=\"2\"/>\n  <path d=\"M44,80 Q60,88 76,80 Z\" fill=\"#ffffff\"/>\n  <path d=\"M22,66 L28,62 L32,68 L26,72 Z\" fill=\"#38bdf8\"/>\n  <path d=\"M98,66 L92,62 L88,68 L94,72 Z\" fill=\"#38bdf8\"/>\n  <polygon points=\"60,96 63,102 69,103 64,107 66,113 60,109 54,113 56,107 51,103 57,102\" fill=\"#0284c7\"/>\n</svg>"
  },
  {
    "id": "brook",
    "name": "Brook",
    "role": "Músico",
    "icon": "💀",
    "sound": "brook",
    "color": "#475569",
    "bgLight": "#f8fafc",
    "border": "#94a3b8",
    "title": "¡YOHOHOHO! ¡CASI ME DA UN ATAQUE AL CORAZÓN!",
    "quotes": [
      "¡YOHOHOHO! ¡Casi me da un ataque al corazón al ver esa opción!... Aunque yo ya estoy muerto, ¡yohohoho! ¡Skull Joke!",
      "¡Mis ojos no dan crédito a semejante fallo!... ¡Aunque yo no tengo ojos! ¡YOHOHOHO!",
      "Binks no Sake sonaría tristísimo si se pierden las tablas por esa sentencia. ¡Toquemos un réquiem por esos datos!",
      "¡Soul Solid! Se me congelaron los huesos al ver cómo dejaste desprotegido ese host de conexión... ¡Y eso que solo soy huesos!",
      "¡Yohohoho! Me dolería el estómago de la risa por esa respuesta... ¡si tan solo tuviera estómago!",
      "Una partitura sin notas no es música, ¡y un usuario sin contraseña es un suicidio de seguridad!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <circle cx=\"60\" cy=\"54\" r=\"44\" fill=\"#09090b\"/>\n  <ellipse cx=\"60\" cy=\"24\" rx=\"28\" ry=\"8\" fill=\"#18181b\"/>\n  <rect x=\"42\" y=\"6\" width=\"36\" height=\"20\" rx=\"3\" fill=\"#18181b\"/>\n  <rect x=\"42\" y=\"20\" width=\"36\" height=\"4\" fill=\"#e11d48\"/>\n  <ellipse cx=\"60\" cy=\"68\" rx=\"26\" ry=\"28\" fill=\"#f8fafc\" stroke=\"#cbd5e1\" stroke-width=\"2\"/>\n  <ellipse cx=\"48\" cy=\"60\" rx=\"8\" ry=\"10\" fill=\"#09090b\"/>\n  <ellipse cx=\"72\" cy=\"60\" rx=\"8\" ry=\"10\" fill=\"#09090b\"/>\n  <polygon points=\"60,68 57,74 63,74\" fill=\"#09090b\"/>\n  <path d=\"M42,78 Q60,88 78,78 Q60,94 42,78 Z\" fill=\"#09090b\"/>\n  <line x1=\"48\" y1=\"80\" x2=\"48\" y2=\"86\" stroke=\"#f8fafc\" stroke-width=\"2\"/>\n  <line x1=\"54\" y1=\"80\" x2=\"54\" y2=\"87\" stroke=\"#f8fafc\" stroke-width=\"2\"/>\n  <line x1=\"60\" y1=\"80\" x2=\"60\" y2=\"88\" stroke=\"#f8fafc\" stroke-width=\"2\"/>\n  <line x1=\"66\" y1=\"80\" x2=\"66\" y2=\"87\" stroke=\"#f8fafc\" stroke-width=\"2\"/>\n  <line x1=\"72\" y1=\"80\" x2=\"72\" y2=\"80\" stroke=\"#f8fafc\" stroke-width=\"2\"/>\n  <path d=\"M38,50 L46,54\" stroke=\"#cbd5e1\" stroke-width=\"2\"/>\n</svg>"
  },
  {
    "id": "jinbe",
    "name": "Jinbe",
    "role": "Timonel",
    "icon": "🥋",
    "sound": "jinbe",
    "color": "#0284c7",
    "bgLight": "#f0f9ff",
    "border": "#38bdf8",
    "title": "¡MANTÉN LA CALMA Y EL TIMÓN FIRME!",
    "quotes": [
      "¡Gyojin Karate: Onda Marina! Mantén la calma y el honor, nakama. Un verdadero timonel nunca pierde el rumbo por un fallo.",
      "Dejaste el timón suelto en medio de una tormenta de inyecciones SQL. ¡Corrige la dirección de inmediato!",
      "La experiencia en el mar enseña que un privilegio mal otorgado es como una vía de agua en el casco del barco.",
      "No pierdas la concentración, joven pirata. La disciplina en la auditoría salvará a tu tripulación.",
      "Aceptar el error es el primer paso para dominar las corrientes más turbulentas de MySQL.",
      "¡Ni la Marina ni los piratas más despiadados vulnerarán tus datos si mantienes tus políticas firmes!"
    ],
    "svg": "<svg viewBox=\"0 0 120 120\" width=\"105\" height=\"105\" xmlns=\"http://www.w3.org/2000/svg\">\n  <path d=\"M20,50 Q16,14 60,14 Q104,14 100,50 Q96,80 88,86 Q60,60 32,86 Q24,80 20,50 Z\" fill=\"#0f172a\"/>\n  <ellipse cx=\"60\" cy=\"65\" rx=\"36\" ry=\"32\" fill=\"#38bdf8\"/>\n  <path d=\"M32,46 Q40,36 48,42 Q52,38 56,44\" stroke=\"#ffffff\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n  <path d=\"M88,46 Q80,36 72,42 Q68,38 64,44\" stroke=\"#ffffff\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n  <ellipse cx=\"44\" cy=\"54\" rx=\"4\" ry=\"4\" fill=\"#0f172a\"/>\n  <circle cx=\"45\" cy=\"53\" r=\"1.5\" fill=\"#ffffff\"/>\n  <ellipse cx=\"76\" cy=\"54\" rx=\"4\" ry=\"4\" fill=\"#0f172a\"/>\n  <circle cx=\"77\" cy=\"53\" r=\"1.5\" fill=\"#ffffff\"/>\n  <ellipse cx=\"60\" cy=\"58\" rx=\"8\" ry=\"4\" fill=\"#0284c7\"/>\n  <path d=\"M40,74 Q60,84 80,74\" stroke=\"#0f172a\" stroke-width=\"3\" fill=\"none\"/>\n  <polygon points=\"46,74 50,66 54,75\" fill=\"#ffffff\" stroke=\"#0f172a\" stroke-width=\"1.5\"/>\n  <polygon points=\"66,75 70,66 74,74\" fill=\"#ffffff\" stroke=\"#0f172a\" stroke-width=\"1.5\"/>\n  <circle cx=\"60\" cy=\"88\" r=\"8\" fill=\"#dc2626\"/>\n  <circle cx=\"60\" cy=\"88\" r=\"4\" fill=\"#38bdf8\"/>\n</svg>"
  }
]

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def leer_resultados():
    if not os.path.exists(RESULTADOS_FILE):
        return []
    try:
        with open(RESULTADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_resultado(resultado):
    resultados = leer_resultados()
    existente = next((r for r in resultados if r.get("carne") == resultado.get("carne")), None)
    if existente:
        resultados.remove(existente)
    resultados.append(resultado)
    
    with open(RESULTADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    return len(resultados)

def eliminar_resultado_alumno(carne):
    resultados = leer_resultados()
    nuevos = [r for r in resultados if r.get("carne") != carne]
    with open(RESULTADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(nuevos, f, ensure_ascii=False, indent=2)
    return len(resultados) != len(nuevos)

# ==============================================================================
# PLANTILLA HTML ALUMNO — NEUMORPHISM + ANTI-REINTENTOS + RESUME EN F5
# ==============================================================================
HTML_ALUMNO = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evaluación Oficial — Seguridad Lógica MySQL</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #e9ecf4;
      --card-bg: #e9ecf4;
      --shadow-light: #ffffff;
      --shadow-dark: #c8d0e0;
      --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      --primary-color: #5551ff;
      --text-main: #2d3748;
      --text-muted: #718096;
      --success: #10b981;
      --danger: #ef4444;
      --radius-lg: 28px;
      --radius-md: 18px;
      --radius-sm: 12px;
      --radius-pill: 9999px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
      overflow-x: hidden;
    }}

    #confetti-canvas {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 9999;
      display: none;
    }}

    .container {{
      width: 100%;
      max-width: 860px;
    }}

    .card {{
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      padding: 44px 38px;
      box-shadow: 14px 14px 30px var(--shadow-dark), -14px -14px 30px var(--shadow-light);
      position: relative;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      border-radius: var(--radius-pill);
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: var(--card-bg);
      color: var(--primary-color);
      box-shadow: 4px 4px 10px var(--shadow-dark), -4px -4px 10px var(--shadow-light);
      margin-bottom: 16px;
    }}

    .title {{
      font-size: 2.1rem;
      font-weight: 800;
      color: #1a202c;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}

    .subtitle {{
      color: var(--text-muted);
      font-size: 0.98rem;
      margin-bottom: 28px;
    }}

    .form-group {{
      margin-bottom: 24px;
      text-align: left;
    }}

    .form-label {{
      display: block;
      font-size: 0.85rem;
      font-weight: 700;
      color: #4a5568;
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .form-input {{
      width: 100%;
      padding: 16px 20px;
      background: var(--card-bg);
      border: none;
      outline: none;
      border-radius: var(--radius-md);
      color: #2d3748;
      font-size: 1rem;
      font-family: inherit;
      box-shadow: inset 5px 5px 10px var(--shadow-dark), inset -5px -5px 10px var(--shadow-light);
      transition: all 0.25s ease;
    }}

    .form-input:focus {{
      box-shadow: inset 6px 6px 12px var(--shadow-dark), inset -6px -6px 12px var(--shadow-light), 0 0 0 2px rgba(99, 102, 241, 0.4);
    }}

    .info-panel {{
      background: var(--card-bg);
      border-radius: var(--radius-md);
      padding: 20px 22px;
      margin-bottom: 28px;
      font-size: 0.92rem;
      color: #4a5568;
      line-height: 1.6;
      box-shadow: inset 3px 3px 8px var(--shadow-dark), inset -3px -3px 8px var(--shadow-light);
    }}

    .alert-locked {{
      background: #fef2f2;
      border-left: 5px solid var(--danger);
      border-radius: var(--radius-md);
      padding: 20px 22px;
      margin-bottom: 24px;
      font-size: 0.95rem;
      color: #991b1b;
      line-height: 1.6;
      box-shadow: 4px 4px 10px var(--shadow-dark), -4px -4px 10px var(--shadow-light);
      display: none;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      width: 100%;
      padding: 18px 28px;
      border-radius: var(--radius-pill);
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      border: none;
      outline: none;
      font-family: inherit;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .btn-primary {{
      background: var(--primary-gradient);
      color: #ffffff;
      box-shadow: 8px 8px 18px rgba(79, 70, 229, 0.35), -6px -6px 14px var(--shadow-light);
    }}

    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 10px 10px 22px rgba(79, 70, 229, 0.45), -6px -6px 14px var(--shadow-light);
    }}

    .btn-primary:active {{
      transform: translateY(1px);
      box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.3);
    }}

    .btn-primary:disabled {{
      opacity: 0.55;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }}

    .hud {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .hud-pill {{
      background: var(--card-bg);
      padding: 10px 18px;
      border-radius: var(--radius-pill);
      font-size: 0.88rem;
      font-weight: 700;
      color: #4a5568;
      box-shadow: 5px 5px 12px var(--shadow-dark), -5px -5px 12px var(--shadow-light);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .progress-track {{
      height: 12px;
      background: var(--card-bg);
      border-radius: var(--radius-pill);
      box-shadow: inset 3px 3px 7px var(--shadow-dark), inset -3px -3px 7px var(--shadow-light);
      overflow: hidden;
      margin-bottom: 28px;
      position: relative;
    }}

    .progress-fill {{
      height: 100%;
      background: var(--primary-gradient);
      width: 0%;
      border-radius: var(--radius-pill);
      transition: width 0.35s ease;
      box-shadow: 2px 0 8px rgba(99, 102, 241, 0.4);
    }}

    .q-section {{
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--primary-color);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 12px;
    }}

    .q-title {{
      font-size: 1.3rem;
      font-weight: 700;
      line-height: 1.5;
      color: #1a202c;
      margin-bottom: 20px;
      white-space: pre-line;
    }}

    .sql-code {{
      background: #1e2538;
      border-radius: var(--radius-md);
      padding: 16px 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.92rem;
      color: #38bdf8;
      overflow-x: auto;
      margin: 14px 0 24px 0;
      line-height: 1.6;
      box-shadow: inset 4px 4px 10px rgba(0, 0, 0, 0.5);
    }}

    .options-grid {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 30px;
    }}

    .option-btn {{
      display: flex;
      align-items: flex-start;
      gap: 16px;
      width: 100%;
      padding: 18px 20px;
      background: var(--card-bg);
      border: 2px solid transparent;
      outline: none;
      border-radius: var(--radius-md);
      color: #2d3748;
      text-align: left;
      font-size: 1rem;
      font-family: inherit;
      cursor: pointer;
      box-shadow: 6px 6px 14px var(--shadow-dark), -6px -6px 14px var(--shadow-light);
      transition: all 0.2s ease;
      line-height: 1.45;
    }}

    .option-btn:hover:not(:disabled) {{
      transform: translateY(-2px);
      box-shadow: 8px 8px 18px var(--shadow-dark), -8px -8px 18px var(--shadow-light);
    }}

    .option-letter {{
      min-width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--card-bg);
      font-weight: 800;
      font-size: 0.95rem;
      color: var(--primary-color);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 3px 3px 7px var(--shadow-dark), -3px -3px 7px var(--shadow-light);
      transition: all 0.2s ease;
    }}

    .option-btn.correct-choice {{
      box-shadow: inset 4px 4px 10px rgba(16, 185, 129, 0.2), inset -4px -4px 10px #ffffff, 0 0 18px rgba(16, 185, 129, 0.35) !important;
      border-color: var(--success) !important;
      background: #e6f9f2 !important;
    }}
    .option-btn.correct-choice .option-letter {{
      background: var(--success) !important;
      color: #fff !important;
      box-shadow: 2px 2px 8px rgba(16, 185, 129, 0.4) !important;
    }}

    .option-btn.wrong-choice {{
      box-shadow: inset 4px 4px 10px rgba(239, 68, 68, 0.2), inset -4px -4px 10px #ffffff !important;
      border-color: var(--danger) !important;
      background: #fde8e8 !important;
      animation: shakeWobble 0.45s ease;
    }}
    .option-btn.wrong-choice .option-letter {{
      background: var(--danger) !important;
      color: #fff !important;
      box-shadow: 2px 2px 8px rgba(239, 68, 68, 0.4) !important;
    }}

    @keyframes shakeWobble {{
      0%, 100% {{ transform: translateX(0); }}
      20% {{ transform: translateX(-10px) rotate(-1deg); }}
      40% {{ transform: translateX(10px) rotate(1deg); }}
      60% {{ transform: translateX(-8px) rotate(-1deg); }}
      80% {{ transform: translateX(8px) rotate(1deg); }}
    }}

    .nav-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      flex-wrap: wrap;
      gap: 14px;
    }}

    /* MODAL CÓMICO DE LA TRIPULACIÓN MUGIWARA */
    .luffy-overlay {{
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(6px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      padding: 20px;
    }}

    .luffy-card {{
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      max-width: 520px;
      width: 100%;
      padding: 30px 24px;
      text-align: center;
      box-shadow: 18px 18px 45px rgba(0,0,0,0.35), -12px -12px 30px var(--shadow-light);
      animation: luffyBounceIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
      position: relative;
    }}

    @keyframes luffyBounceIn {{
      0% {{ transform: scale(0.65) rotate(-6deg); opacity: 0; }}
      65% {{ transform: scale(1.08) rotate(3deg); opacity: 1; }}
      100% {{ transform: scale(1) rotate(0deg); }}
    }}

    .crew-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 16px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      margin-bottom: 12px;
      box-shadow: inset 2px 2px 5px var(--shadow-dark), inset -2px -2px 5px var(--shadow-light);
      transition: all 0.3s ease;
    }}

    .luffy-avatar-box {{
      width: 122px;
      height: 122px;
      border-radius: 50%;
      margin: 0 auto 14px auto;
      background: var(--card-bg);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 6px 6px 14px var(--shadow-dark), -6px -6px 14px var(--shadow-light);
      animation: luffyLaughRock 2s infinite ease-in-out;
      overflow: hidden;
    }}

    @keyframes luffyLaughRock {{
      0%, 100% {{ transform: rotate(-3deg) scale(1); }}
      50% {{ transform: rotate(3deg) scale(1.04); }}
    }}

    .luffy-title {{
      font-size: 1.3rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: color 0.3s ease;
    }}

    .luffy-bubble {{
      border-radius: var(--radius-md);
      padding: 16px 20px;
      font-size: 1.02rem;
      font-weight: 700;
      line-height: 1.5;
      margin-bottom: 18px;
      box-shadow: inset 2px 2px 6px rgba(0,0,0,0.06);
      transition: all 0.3s ease;
      min-height: 65px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .correct-reminder {{
      font-size: 0.95rem;
      color: #4a5568;
      margin-bottom: 22px;
      font-weight: 600;
      background: #f8fafc;
      padding: 10px 14px;
      border-radius: 10px;
      border: 1px solid #e2e8f0;
    }}

    /* Pantalla Resultados */
    .score-circle {{
      width: 150px;
      height: 150px;
      border-radius: 50%;
      margin: 24px auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: var(--card-bg);
      box-shadow: 10px 10px 24px var(--shadow-dark), -10px -10px 24px var(--shadow-light);
    }}

    .score-num {{
      font-size: 3rem;
      font-weight: 800;
      line-height: 1;
      background: var(--primary-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .score-total {{
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 700;
      margin-top: 4px;
    }}

    .stats-summary {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 28px 0;
    }}

    .stat-box {{
      background: var(--card-bg);
      border-radius: var(--radius-md);
      padding: 18px 14px;
      text-align: center;
      box-shadow: 6px 6px 14px var(--shadow-dark), -6px -6px 14px var(--shadow-light);
    }}

    .stat-val {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #1a202c;
    }}

    .stat-lbl {{
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      margin-top: 6px;
      letter-spacing: 0.04em;
    }}

    .notice-box {{
      background: var(--card-bg);
      padding: 18px;
      border-radius: var(--radius-md);
      color: var(--success);
      font-weight: 700;
      margin-bottom: 26px;
      text-align: center;
      box-shadow: inset 4px 4px 9px var(--shadow-dark), inset -4px -4px 9px var(--shadow-light);
    }}
  </style>
</head>
<body>

<canvas id="confetti-canvas"></canvas>

<div class="container">
  
  <!-- SCREEN 1: REGISTRO DEL ALUMNO -->
  <div id="screen-reg" class="card">
    <div style="text-align: center;">
      <div class="badge">🛡️ Evaluación Oficial • MySQL 8.0</div>
      <h1 class="title">Seguridad Lógica en Bases de Datos</h1>
      <p class="subtitle">Asignatura: Auditoría de Sistemas Informáticos • 30 Preguntas</p>
    </div>

    <!-- Alerta si el alumno ya completó su examen -->
    <div id="alert-locked" class="alert-locked"></div>

    <div class="form-group">
      <label class="form-label">Nombre Completo del Estudiante</label>
      <input type="text" id="reg-name" class="form-input" placeholder="Ingresa tus nombres y apellidos" autofocus>
    </div>

    <div class="form-group">
      <label class="form-label">Número de Carné Universitario</label>
      <input type="text" id="reg-id" class="form-input" placeholder="Ej: US-2024-001">
    </div>

    <div class="info-panel">
      🔒 <b>Seguridad de la Evaluación:</b><br>
      • Cada carné tiene permitida <b>UNA SOLA ENTREGA OFICIAL</b>.<br>
      • Si recargas la página (F5) o se cierra la pestaña, <b>tu progreso se restaurará exactamente en la pregunta donde ibas</b>; no podrás volver a contestar las preguntas anteriores.<br>
      • Al responder la última pregunta, tu calificación se cerrará permanentemente en el servidor.
    </div>

    <button class="btn btn-primary" id="btn-start" onclick="iniciarExamen()">
      <span>Comenzar Evaluación Oficial</span>
      <span>➔</span>
    </button>
  </div>

  <!-- SCREEN 2: PREGUNTAS -->
  <div id="screen-exam" class="card" style="display: none;">
    <div class="hud">
      <div class="hud-pill">👤 <span id="hud-name"></span> (<span id="hud-id"></span>)</div>
      <div class="hud-pill">⏱️ <span id="hud-time" style="font-family: 'JetBrains Mono', monospace; color: var(--primary-color);">00:00</span></div>
    </div>

    <div class="progress-track">
      <div class="progress-fill" id="progress-fill"></div>
    </div>

    <div class="q-section" id="q-section">SECCIÓN</div>
    <div class="q-title" id="q-text">Pregunta...</div>
    <div id="q-code" class="sql-code" style="display: none;"></div>

    <div class="options-grid" id="options-container"></div>

    <div class="nav-actions">
      <div class="hud-pill" style="box-shadow: inset 3px 3px 6px var(--shadow-dark), inset -3px -3px 6px var(--shadow-light);" id="q-counter">
        Pregunta 1 de 30
      </div>
      <button class="btn btn-primary" id="btn-next" style="width: auto; padding: 14px 32px; display: none;" onclick="siguientePregunta()">
        <span id="btn-next-text">Siguiente Pregunta</span>
        <span>➔</span>
      </button>
    </div>
  </div>

  <!-- SCREEN 3: RESULTADO FINAL -->
  <div id="screen-result" class="card" style="display: none; text-align: center;">
    <div class="badge">Entrega Confirmada</div>
    <h2 class="title">¡Evaluación Registrada!</h2>
    
    <div class="notice-box">
      ✓ Tus respuestas han sido recibidas y almacenadas exitosamente por el docente.
    </div>

    <div class="score-circle">
      <div class="score-num" id="res-score">10.0</div>
      <div class="score-total">de 10.0 pts</div>
    </div>

    <div class="stats-summary">
      <div class="stat-box">
        <div class="stat-val" id="stat-correct" style="color: var(--success);">0</div>
        <div class="stat-lbl">Aciertos (de 30)</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" id="stat-wrong" style="color: var(--danger);">0</div>
        <div class="stat-lbl">Fallos</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" id="stat-time" style="color: var(--primary-color);">00:00</div>
        <div class="stat-lbl">Tiempo Empleado</div>
      </div>
    </div>

    <p style="font-size: 0.95rem; color: var(--text-muted); margin-top: 10px;">
      Tu examen ha quedado cerrado oficialmente. Puedes cerrar esta ventana.
    </p>
  </div>

</div>

<!-- MODAL CÓMICO DE LA TRIPULACIÓN MUGIWARA -->
<div id="luffy-modal" class="luffy-overlay">
  <div class="luffy-card">
    <div id="crew-tag" class="crew-badge">
      👒 Monkey D. Luffy — Capitán
    </div>

    <div class="luffy-avatar-box" id="crew-avatar-box">
      <!-- Avatar dinámico inyectado por JS -->
    </div>

    <div class="luffy-title" id="crew-title">
      <span>👒</span>
      <span>¡SHISHISHI! ¡FALLASTE LA CONSULTA, NAKAMA!</span>
    </div>

    <div class="luffy-bubble" id="luffy-quote">
      "¡SHISHISHI! ¡Ni activando el Gear 5 salvaste esa consulta, nakama!"
    </div>

    <div class="correct-reminder" id="luffy-correct-note">
      La respuesta correcta era la opción <b>B</b>.
    </div>

    <button class="btn btn-primary" id="crew-modal-btn" onclick="cerrarLuffyModal()">
      <span>¡Continuar Navegando!</span>
      <span>➔</span>
    </button>
  </div>
</div>

<script>
  const PREGUNTAS = {json.dumps(PREGUNTAS_DATA, ensure_ascii=False)};
  let studentName = "";
  let studentId = "";
  let currentIndex = 0;
  let userAnswers = [];
  let timerInterval = null;
  let totalSeconds = 0;
  let yaRespondioActual = false;
  let examenEnCurso = false;

  const STORAGE_KEY = "sql_exam_active_session";

    const MUGIWARA_CREW = {json.dumps(MUGIWARA_CREW_DATA, ensure_ascii=False)};
  let barajaChistes = [];
  let ultimoPersonajeId = null;

  function inicializarBarajaPerfecta() {{
    const quotesPool = {{}};
    MUGIWARA_CREW.forEach(c => {{
      quotesPool[c.id] = [...c.quotes];
      for (let i = quotesPool[c.id].length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [quotesPool[c.id][i], quotesPool[c.id][j]] = [quotesPool[c.id][j], quotesPool[c.id][i]];
      }}
    }});

    const baraja = [];
    let ultimoIdRonda = null;

    let quedenFrases = true;
    while (quedenFrases) {{
      const disponibles = MUGIWARA_CREW.filter(c => quotesPool[c.id].length > 0).map(c => c.id);
      if (disponibles.length === 0) break;

      for (let i = disponibles.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [disponibles[i], disponibles[j]] = [disponibles[j], disponibles[i]];
      }}

      if (disponibles.length > 1 && disponibles[0] === ultimoIdRonda) {{
        const temp = disponibles[0];
        disponibles[0] = disponibles[disponibles.length - 1];
        disponibles[disponibles.length - 1] = temp;
      }}

      disponibles.forEach(charId => {{
        const quote = quotesPool[charId].pop();
        baraja.push({{ charId, quote }});
        ultimoIdRonda = charId;
      }});
    }}

    barajaChistes = baraja;
  }}

  function obtenerSiguienteChiste() {{
    if (!barajaChistes || barajaChistes.length === 0) {{
      inicializarBarajaPerfecta();
    }}

    let idx = 0;
    if (barajaChistes.length > 1 && barajaChistes[0].charId === ultimoPersonajeId) {{
      for (let i = 1; i < barajaChistes.length; i++) {{
        if (barajaChistes[i].charId !== ultimoPersonajeId) {{
          idx = i;
          break;
        }}
      }}
    }}

    const [item] = barajaChistes.splice(idx, 1);
    ultimoPersonajeId = item.charId;
    const char = MUGIWARA_CREW.find(c => c.id === item.charId);
    return {{ char, quote: item.quote }};
  }}

  // ADVERTENCIA AL INTENTAR SALIR O RECARGAR
  window.addEventListener("beforeunload", function (e) {{
    if (examenEnCurso) {{
      e.preventDefault();
      e.returnValue = "Tienes una evaluación en curso. Tus respuestas ya guardadas se mantendrán, pero no podrás repetir las anteriores.";
    }}
  }});

  // VERIFICAR SESIÓN PREVIA O REANUDAR EN CASO DE RECARGA (F5)
  window.addEventListener("load", function () {{
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {{
      try {{
        const state = JSON.parse(saved);
        if (state && state.carne && state.userAnswers) {{
          // Verificar si ya fue entregado en el servidor
          fetch(`/api/estado_alumno?carne=${{encodeURIComponent(state.carne)}}`)
            .then(res => res.json())
            .then(data => {{
              if (data.entregado) {{
                localStorage.removeItem(STORAGE_KEY);
                mostrarAlertaBloqueado(state.carne, data.resultado);
              }} else {{
                // REANUDAR SESIÓN EXACTAMENTE DONDE SE QUEDÓ
                studentName = state.nombre;
                studentId = state.carne;
                currentIndex = state.currentIndex || 0;
                userAnswers = state.userAnswers || [];
                totalSeconds = state.totalSeconds || 0;
                if (state.barajaChistes && state.barajaChistes.length > 0) {{
                  barajaChistes = state.barajaChistes;
                  ultimoPersonajeId = state.ultimoPersonajeId || null;
                }} else {{
                  inicializarBarajaPerfecta();
                }}
                
                document.getElementById("hud-name").innerText = studentName;
                document.getElementById("hud-id").innerText = studentId;

                iniciarCronometro();
                examenEnCurso = true;

                document.getElementById("screen-reg").style.display = "none";
                document.getElementById("screen-exam").style.display = "block";

                alert(`ℹ️ Sesión reanudada para ${{studentName}}. Retomas en la pregunta ${{currentIndex + 1}} de ${{PREGUNTAS.length}}. Las respuestas anteriores ya quedaron fijadas.`);
                cargarPregunta();
              }}
            }})
            .catch(() => {{}});
        }}
      }} catch (e) {{
        localStorage.removeItem(STORAGE_KEY);
      }}
    }}
  }});

  function guardarEstadoLocal() {{
    const state = {{
      nombre: studentName,
      carne: studentId,
      currentIndex: currentIndex,
      userAnswers: userAnswers,
      totalSeconds: totalSeconds,
      barajaChistes: barajaChistes,
      ultimoPersonajeId: ultimoPersonajeId,
      timestamp: Date.now()
    }};
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }}

  function mostrarAlertaBloqueado(carne, resultado) {{
    const alertBox = document.getElementById("alert-locked");
    alertBox.style.display = "block";
    alertBox.innerHTML = `
      <b>⚠️ EVALUACIÓN YA COMPLETADA:</b><br>
      El carné <b>${{carne}}</b> ya tiene una evaluación entregada y calificada en el servidor.<br>
      • <b>Nota registrada:</b> ${{resultado.nota}} / 10 pts (${{resultado.aciertos}} aciertos).<br>
      • <b>Fecha de entrega:</b> ${{resultado.fecha_hora}}.<br><br>
      <i>No se permiten reintentos. Si necesitas una reposición, solicita la autorización directa del docente.</i>
    `;
    document.getElementById("btn-start").disabled = true;
  }}

  // SINTETIZADOR DE AUDIO
  let audioCtx = null;
  function getAudioCtx() {{
    if (!audioCtx) {{
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }}
    return audioCtx;
  }}

  function playSound(type) {{
    try {{
      const ctx = getAudioCtx();
      if (!ctx) return;
      if (ctx.state === 'suspended') ctx.resume();

      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'correct') {{
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.setValueAtTime(659.25, now + 0.08);
        osc.frequency.setValueAtTime(783.99, now + 0.16);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
      }} else if (type === 'luffy') {{
        // Bouncing laugh / Gear 5
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(340, now);
        osc.frequency.exponentialRampToValueAtTime(110, now + 0.35);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now);
        osc.stop(now + 0.38);
      }} else if (type === 'zoro') {{
        // Sharp sword slash
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(820, now);
        osc.frequency.exponentialRampToValueAtTime(90, now + 0.25);
        gain.gain.setValueAtTime(0.22, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
        osc.start(now);
        osc.stop(now + 0.28);
      }} else if (type === 'nami') {{
        // Berries money chime
        osc.type = 'sine';
        osc.frequency.setValueAtTime(987.77, now);
        osc.frequency.setValueAtTime(1318.51, now + 0.09);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now);
        osc.stop(now + 0.38);
      }} else if (type === 'usopp') {{
        // Slingshot boing
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.exponentialRampToValueAtTime(640, now + 0.18);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
        osc.start(now);
        osc.stop(now + 0.32);
      }} else if (type === 'sanji') {{
        // Diable jamble fire sizzle
        osc.type = 'square';
        osc.frequency.setValueAtTime(280, now);
        osc.frequency.linearRampToValueAtTime(130, now + 0.28);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
      }} else if (type === 'chopper') {{
        // Cute panic squeak
        osc.type = 'sine';
        osc.frequency.setValueAtTime(580, now);
        osc.frequency.linearRampToValueAtTime(880, now + 0.12);
        osc.frequency.linearRampToValueAtTime(440, now + 0.28);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
      }} else if (type === 'robin') {{
        // Flower bloom mystery chime
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.setValueAtTime(554.37, now + 0.1);
        osc.frequency.setValueAtTime(659.25, now + 0.2);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.42);
        osc.start(now);
        osc.stop(now + 0.42);
      }} else if (type === 'franky') {{
        // SUUUUPER brass blast
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.setValueAtTime(330, now + 0.08);
        osc.frequency.setValueAtTime(440, now + 0.16);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.42);
        osc.start(now);
        osc.stop(now + 0.42);
      }} else if (type === 'brook') {{
        // Yohoho violin skull pluck
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.linearRampToValueAtTime(220, now + 0.14);
        osc.frequency.linearRampToValueAtTime(330, now + 0.28);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now);
        osc.stop(now + 0.38);
      }} else if (type === 'jinbe') {{
        // Deep gyojin wave gong
        osc.type = 'sine';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(55, now + 0.38);
        gain.gain.setValueAtTime(0.24, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.42);
        osc.start(now);
        osc.stop(now + 0.42);
      }}
    }} catch (e) {{}}
  }}

  // MOTOR DE CONFETI VERDE
  function lanzarConfetiVerde() {{
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.display = 'block';

    const particles = [];
    const colors = ['#10b981', '#34d399', '#059669', '#6ee7b7', '#a7f3d0', '#fbbf24', '#4ade80'];

    for (let i = 0; i < 75; i++) {{
      particles.push({{
        x: canvas.width / 2 + (Math.random() - 0.5) * 240,
        y: canvas.height * 0.45,
        vx: (Math.random() - 0.5) * 16,
        vy: Math.random() * -14 - 4,
        size: Math.random() * 9 + 6,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        vRot: (Math.random() - 0.5) * 12,
        opacity: 1
      }});
    }}

    const startTime = Date.now();
    function animate() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = false;
      particles.forEach(p => {{
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.45;
        p.rotation += p.vRot;
        p.opacity -= 0.013;

        if (p.opacity > 0 && p.y < canvas.height) {{
          alive = true;
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = Math.max(0, p.opacity);
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
          ctx.restore();
        }}
      }});

      if (alive && Date.now() - startTime < 2200) {{
        requestAnimationFrame(animate);
      }} else {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        canvas.style.display = 'none';
      }}
    }}
    requestAnimationFrame(animate);
  }}

  function iniciarCronometro() {{
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {{
      totalSeconds++;
      const mins = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
      const secs = String(totalSeconds % 60).padStart(2, "0");
      document.getElementById("hud-time").innerText = `${{mins}}:${{secs}}`;
      if (totalSeconds % 5 === 0) guardarEstadoLocal();
    }}, 1000);
  }}

  function iniciarExamen() {{
    const name = document.getElementById("reg-name").value.trim();
    const id = document.getElementById("reg-id").value.trim().toUpperCase();

    if (!name || !id) {{
      alert("Por favor ingresa tu nombre completo y carné para continuar.");
      return;
    }}

    // VALIDAR CON EL SERVIDOR SI YA ENTREGÓ
    fetch(`/api/estado_alumno?carne=${{encodeURIComponent(id)}}`)
      .then(res => res.json())
      .then(data => {{
        if (data.entregado) {{
          mostrarAlertaBloqueado(id, data.resultado);
          return;
        }}

        studentName = name;
        studentId = id;

        document.getElementById("hud-name").innerText = studentName;
        document.getElementById("hud-id").innerText = studentId;

        currentIndex = 0;
        userAnswers = [];
        totalSeconds = 0;
        examenEnCurso = true;
        inicializarBarajaPerfecta();

        guardarEstadoLocal();
        iniciarCronometro();

        document.getElementById("screen-reg").style.display = "none";
        document.getElementById("screen-exam").style.display = "block";
        cargarPregunta();
      }})
      .catch(err => {{
        alert("Error de conexión con el servidor del docente. Asegúrate de estar conectado.");
      }});
  }}

  function cargarPregunta() {{
    yaRespondioActual = false;
    const q = PREGUNTAS[currentIndex];
    
    document.getElementById("q-section").innerText = `${{q.seccion}}`;
    document.getElementById("q-counter").innerText = `Pregunta ${{currentIndex + 1}} de ${{PREGUNTAS.length}}`;

    const progress = ((currentIndex) / PREGUNTAS.length) * 100;
    document.getElementById("progress-fill").style.width = `${{progress}}%`;

    const qTextEl = document.getElementById("q-text");
    const qCodeEl = document.getElementById("q-code");

    if (q.enunciado.includes("SELECT") || q.enunciado.includes("GRANT") || q.enunciado.includes("FROM")) {{
      const parts = q.enunciado.split(/\\n\\n+/);
      if (parts.length >= 3) {{
        qTextEl.innerText = parts[0] + "\\n" + parts[2];
        qCodeEl.innerText = parts[1];
        qCodeEl.style.display = "block";
      }} else {{
        qTextEl.innerText = q.enunciado;
        qCodeEl.style.display = "none";
      }}
    }} else {{
      qTextEl.innerText = q.enunciado;
      qCodeEl.style.display = "none";
    }}

    const container = document.getElementById("options-container");
    container.innerHTML = "";

    q.opciones.forEach(op => {{
      const btn = document.createElement("button");
      btn.className = "option-btn";
      btn.innerHTML = `
        <span class="option-letter">${{op.letra}}</span>
        <span class="option-text">${{op.texto}}</span>
      `;
      btn.onclick = () => responderPregunta(op.letra, btn);
      container.appendChild(btn);
    }});

    const btnNext = document.getElementById("btn-next");
    btnNext.style.display = "none";
    const isLast = (currentIndex === PREGUNTAS.length - 1);
    document.getElementById("btn-next-text").innerText = isLast ? "Finalizar y Enviar Evaluación" : "Siguiente Pregunta";
  }}

  function responderPregunta(selectedLetter, clickedBtn) {{
    if (yaRespondioActual) return;
    yaRespondioActual = true;

    const q = PREGUNTAS[currentIndex];
    const isCorrect = (selectedLetter === q.correcta);

    const allBtns = document.querySelectorAll(".option-btn");
    allBtns.forEach(b => b.disabled = true);

    userAnswers.push({{
      id: q.id,
      seccion: q.seccion,
      enunciado: q.enunciado,
      seleccionada: selectedLetter,
      correcta: q.correcta,
      isCorrect: isCorrect
    }});

    // GUARDAR EN LOCALSTORAGE INMEDIATAMENTE
    guardarEstadoLocal();

    if (isCorrect) {{
      clickedBtn.classList.add("correct-choice");
      lanzarConfetiVerde();
      playSound("correct");
      document.getElementById("btn-next").style.display = "inline-flex";
    }} else {{
      clickedBtn.classList.add("wrong-choice");
      allBtns.forEach(b => {{
        const letra = b.querySelector(".option-letter").innerText.trim();
        if (letra === q.correcta) b.classList.add("correct-choice");
      }});

      // Obtener siguiente chiste sin repetición (baraja por rondas)
      const itemChiste = obtenerSiguienteChiste();
      const char = itemChiste.char;
      const randomQuote = itemChiste.quote;

      playSound(char.sound);

      // Personalizar modal con el personaje actual
      const tagEl = document.getElementById("crew-tag");
      tagEl.innerHTML = `${{char.icon}} ${{char.name}} — ${{char.role}}`;
      tagEl.style.color = char.color;
      tagEl.style.background = char.bgLight;
      tagEl.style.border = `1px solid ${{char.border}}`;

      document.getElementById("crew-avatar-box").innerHTML = char.svg;

      const titleEl = document.getElementById("crew-title");
      titleEl.style.color = char.color;
      titleEl.innerHTML = `<span>${{char.icon}}</span> <span>${{char.title}}</span>`;

      const bubbleEl = document.getElementById("luffy-quote");
      bubbleEl.innerText = `"${{randomQuote}}"`;
      bubbleEl.style.background = char.bgLight;
      bubbleEl.style.border = `2px dashed ${{char.border}}`;
      bubbleEl.style.color = char.color;

      document.getElementById("luffy-correct-note").innerHTML = `La respuesta correcta era la opción <b style="color: var(--success); font-size: 1.15rem;">${{q.correcta}}</b>.`;

      const btnEl = document.getElementById("crew-modal-btn");
      btnEl.style.background = `linear-gradient(135deg, ${{char.color}} 0%, #111827 140%)`;

      setTimeout(() => {{
        document.getElementById("luffy-modal").style.display = "flex";
      }}, 320);

      document.getElementById("btn-next").style.display = "inline-flex";
    }}
  }}

  function cerrarLuffyModal() {{
    document.getElementById("luffy-modal").style.display = "none";
    siguientePregunta();
  }}

  function siguientePregunta() {{
    if (currentIndex < PREGUNTAS.length - 1) {{
      currentIndex++;
      guardarEstadoLocal();
      cargarPregunta();
    }} else {{
      finalizarExamen();
    }}
  }}

  function finalizarExamen() {{
    clearInterval(timerInterval);
    examenEnCurso = false;
    document.getElementById("progress-fill").style.width = "100%";

    const correctCount = userAnswers.filter(a => a.isCorrect).length;
    const wrongCount = PREGUNTAS.length - correctCount;
    const rawNota = (correctCount / PREGUNTAS.length) * 10;
    const notaFinal = Math.min(10, Math.max(0, rawNota)).toFixed(1);
    const porcentaje = Math.round((correctCount / PREGUNTAS.length) * 100);

    const mins = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
    const secs = String(totalSeconds % 60).padStart(2, "0");
    const timeStr = `${{mins}}m ${{secs}}s`;

    const payload = {{
      nombre: studentName,
      carne: studentId,
      nota: parseFloat(notaFinal),
      aciertos: correctCount,
      fallos: wrongCount,
      total_preguntas: PREGUNTAS.length,
      porcentaje: porcentaje,
      tiempo: timeStr,
      fecha_hora: new Date().toLocaleString("es-ES"),
      respuestas: userAnswers
    }};

    // ENVIAR AL SERVIDOR Y BORRAR ESTADO LOCAL DE EVALUACIÓN ACTIVA
    fetch("/api/guardar_resultado", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(payload)
    }})
    .then(res => res.json())
    .then(() => {{
      localStorage.removeItem(STORAGE_KEY);
    }})
    .catch(err => console.warn("Aviso de guardado:", err));

    document.getElementById("res-score").innerText = notaFinal;
    document.getElementById("stat-correct").innerText = `${{correctCount}} / ${{PREGUNTAS.length}}`;
    document.getElementById("stat-wrong").innerText = wrongCount;
    document.getElementById("stat-time").innerText = timeStr;

    document.getElementById("screen-exam").style.display = "none";
    document.getElementById("screen-result").style.display = "block";
  }}
</script>

</body>
</html>
'''

# ==============================================================================
# PLANTILLA HTML PANEL DOCENTE — CON BOTÓN "PERMITIR REINTENTO"
# ==============================================================================
HTML_DOCENTE = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Panel del Docente — Auditoría de Sistemas</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #e9ecf4;
      --card-bg: #e9ecf4;
      --shadow-light: #ffffff;
      --shadow-dark: #c8d0e0;
      --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      --primary-color: #5551ff;
      --text-main: #2d3748;
      --text-muted: #718096;
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --radius-lg: 26px;
      --radius-md: 16px;
      --radius-pill: 9999px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      padding: 34px 20px;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}

    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      flex-wrap: wrap;
      gap: 18px;
    }}

    .title {{
      font-size: 1.9rem;
      font-weight: 800;
      color: #1a202c;
      letter-spacing: -0.02em;
    }}

    .subtitle {{
      font-size: 0.98rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      border-radius: var(--radius-pill);
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      border: none;
      outline: none;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      font-family: inherit;
      text-decoration: none;
    }}

    .btn-primary {{
      background: var(--primary-gradient);
      color: #fff;
      box-shadow: 6px 6px 14px rgba(79, 70, 229, 0.35), -4px -4px 10px var(--shadow-light);
    }}
    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 8px 8px 18px rgba(79, 70, 229, 0.45);
    }}
    .btn-primary:active {{
      box-shadow: inset 3px 3px 6px rgba(0,0,0,0.3);
    }}

    .btn-soft {{
      background: var(--card-bg);
      color: #4a5568;
      box-shadow: 5px 5px 12px var(--shadow-dark), -5px -5px 12px var(--shadow-light);
    }}
    .btn-soft:hover {{
      color: var(--primary-color);
      transform: translateY(-2px);
    }}

    .btn-danger {{
      background: var(--card-bg);
      color: var(--danger);
      box-shadow: 5px 5px 12px var(--shadow-dark), -5px -5px 12px var(--shadow-light);
    }}

    .btn-action-unlock {{
      background: var(--card-bg);
      color: var(--warning);
      box-shadow: 3px 3px 8px var(--shadow-dark), -3px -3px 8px var(--shadow-light);
      padding: 6px 12px;
      font-size: 0.8rem;
    }}
    .btn-action-unlock:hover {{
      color: #b45309;
      transform: translateY(-1px);
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }}

    .stat-card {{
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      padding: 24px 22px;
      box-shadow: 8px 8px 20px var(--shadow-dark), -8px -8px 20px var(--shadow-light);
    }}

    .stat-val {{
      font-size: 2.3rem;
      font-weight: 800;
      color: #1a202c;
      line-height: 1.1;
    }}

    .stat-lbl {{
      font-size: 0.82rem;
      text-transform: uppercase;
      color: var(--text-muted);
      font-weight: 700;
      margin-top: 8px;
      letter-spacing: 0.05em;
    }}

    .table-card {{
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: 12px 12px 28px var(--shadow-dark), -12px -12px 28px var(--shadow-light);
    }}

    .table-header {{
      padding: 24px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.96rem;
    }}

    th {{
      padding: 16px 20px;
      background: #e2e6ef;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #4a5568;
      font-weight: 800;
      box-shadow: inset 0 -2px 0 var(--shadow-dark);
    }}

    td {{
      padding: 16px 20px;
      border-bottom: 1px solid #dbe1ed;
      color: #2d3748;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.4);
    }}

    .badge-grade {{
      display: inline-block;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-weight: 800;
      font-size: 0.95rem;
    }}

    .grade-high {{
      background: rgba(16, 185, 129, 0.15);
      color: #059669;
      box-shadow: inset 1px 1px 3px rgba(16, 185, 129, 0.3);
    }}

    .grade-med {{
      background: rgba(245, 158, 11, 0.15);
      color: #d97706;
      box-shadow: inset 1px 1px 3px rgba(245, 158, 11, 0.3);
    }}

    .grade-low {{
      background: rgba(239, 68, 68, 0.15);
      color: #dc2626;
      box-shadow: inset 1px 1px 3px rgba(239, 68, 68, 0.3);
    }}

    .modal-backdrop {{
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(200, 208, 224, 0.6);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 100;
    }}

    .modal-box {{
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      max-width: 820px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 34px;
      box-shadow: 20px 20px 50px var(--shadow-dark), -20px -20px 50px var(--shadow-light);
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 2px solid #dbe1ed;
    }}

    .detail-item {{
      background: var(--card-bg);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-bottom: 14px;
      font-size: 0.92rem;
      box-shadow: 4px 4px 10px var(--shadow-dark), -4px -4px 10px var(--shadow-light);
    }}

    .detail-item.pass {{ border-left: 5px solid var(--success); }}
    .detail-item.fail {{ border-left: 5px solid var(--danger); }}

    .login-container {{
      max-width: 440px;
      margin: 80px auto;
      background: var(--card-bg);
      border-radius: var(--radius-lg);
      padding: 44px 36px;
      text-align: center;
      box-shadow: 14px 14px 32px var(--shadow-dark), -14px -14px 32px var(--shadow-light);
    }}

    .login-icon {{
      width: 80px;
      height: 80px;
      border-radius: 50%;
      margin: 0 auto 20px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.2rem;
      background: var(--card-bg);
      box-shadow: 6px 6px 14px var(--shadow-dark), -6px -6px 14px var(--shadow-light);
    }}

    .input-pin-clear {{
      width: 100%;
      padding: 16px 20px;
      background: var(--card-bg);
      border: none;
      outline: none;
      border-radius: var(--radius-md);
      color: #1a202c;
      font-size: 1.25rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 24px;
      letter-spacing: 0.08em;
      box-shadow: inset 5px 5px 10px var(--shadow-dark), inset -5px -5px 10px var(--shadow-light);
      font-family: inherit;
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- LOGIN LOCK -->
  <div id="login-panel" class="login-container" style="display: block;">
    <div class="login-icon">🔐</div>
    <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 8px;">Panel del Docente</h2>
    <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px;">Ingresa la clave de acceso para ver las calificaciones en tiempo real.</p>
    
    <input type="text" id="input-pin" placeholder="Ingresa PIN" class="input-pin-clear" autofocus>
    
    <button class="btn btn-primary" style="width: 100%; justify-content: center; padding: 16px;" onclick="verificarPIN()">
      <span>Acceder al Panel</span>
      <span>➔</span>
    </button>
  </div>

  <!-- DASHBOARD PRINCIPAL -->
  <div id="dashboard-panel" style="display: none;">
    
    <div class="header">
      <div>
        <h1 class="title">Resultados en Tiempo Real</h1>
        <p class="subtitle">Auditoría de Sistemas • Evaluación de Seguridad Lógica en MySQL</p>
      </div>
      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <button class="btn btn-soft" onclick="cargarResultados()">🔄 Actualizar</button>
        <a href="/api/exportar_csv?pin={PIN_DOCENTE}" class="btn btn-primary">📥 Exportar a Excel (CSV)</a>
        <button class="btn btn-danger" onclick="limpiarResultados()">🗑️ Limpiar Todo</button>
      </div>
    </div>

    <!-- TARJETAS DE RESUMEN (KPIS) -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-val" id="kpi-total">0</div>
        <div class="stat-lbl">Alumnos Evaluados</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" id="kpi-avg" style="color: var(--primary-color);">0.0</div>
        <div class="stat-lbl">Promedio Grupal / 10</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" id="kpi-max" style="color: var(--success);">0.0</div>
        <div class="stat-lbl">Nota Más Alta</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" id="kpi-pass" style="color: #6366f1;">0%</div>
        <div class="stat-lbl">Tasa de Aprobación (≥6.0)</div>
      </div>
    </div>

    <!-- TABLA DE ALUMNOS -->
    <div class="table-card">
      <div class="table-header">
        <h3 style="font-size: 1.15rem; font-weight: 800;">Listado de Evaluaciones Recibidas</h3>
        <span style="font-size: 0.88rem; font-weight: 700; color: var(--success); display: flex; align-items: center; gap: 6px;">
          <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--success); display: inline-block;"></span>
          Monitoreo en vivo activo
        </span>
      </div>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Estudiante</th>
              <th>Carné</th>
              <th>Nota Final</th>
              <th>Aciertos</th>
              <th>Precisión</th>
              <th>Tiempo</th>
              <th>Fecha y Hora</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody id="alumnos-tbody">
            <tr>
              <td colspan="9" style="text-align: center; color: var(--text-muted); padding: 34px;">
                Esperando entregas de los estudiantes...
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

</div>

<!-- MODAL DETALLE EXAMEN ALUMNO -->
<div id="detail-modal" class="modal-backdrop">
  <div class="modal-box">
    <div class="modal-header">
      <div>
        <h2 id="modal-student-name" style="font-size: 1.35rem; font-weight: 800;">Detalle del Estudiante</h2>
        <p id="modal-student-sub" style="color: var(--text-muted); font-size: 0.9rem; margin-top: 4px;"></p>
      </div>
      <button class="btn btn-soft" style="padding: 8px 16px;" onclick="cerrarModal()">✕ Cerrar</button>
    </div>
    <div id="modal-questions-list"></div>
  </div>
</div>

<script>
  let sessionPin = sessionStorage.getItem("docente_pin") || "";
  let cachedResultados = [];

  if (sessionPin === "{PIN_DOCENTE}") {{
    mostrarDashboard();
  }}

  function verificarPIN() {{
    const val = document.getElementById("input-pin").value.trim();
    if (val === "{PIN_DOCENTE}") {{
      sessionStorage.setItem("docente_pin", val);
      sessionPin = val;
      mostrarDashboard();
    }} else {{
      alert("Clave incorrecta. Por favor verifica e intenta de nuevo.");
    }}
  }}

  document.getElementById("input-pin").addEventListener("keydown", function(e) {{
    if (e.key === "Enter") verificarPIN();
  }});

  function mostrarDashboard() {{
    document.getElementById("login-panel").style.display = "none";
    document.getElementById("dashboard-panel").style.display = "block";
    cargarResultados();
    setInterval(cargarResultados, 4000);
  }}

  function cargarResultados() {{
    fetch(`/api/resultados?pin=${{sessionPin}}`)
      .then(res => {{
        if (!res.ok) throw new Error("No autorizado");
        return res.json();
      }})
      .then(data => {{
        cachedResultados = data;
        renderizarTabla(data);
        actualizarKPIs(data);
      }})
      .catch(err => console.warn("Error cargando resultados:", err));
  }}

  function actualizarKPIs(data) {{
    document.getElementById("kpi-total").innerText = data.length;
    if (data.length === 0) {{
      document.getElementById("kpi-avg").innerText = "0.0";
      document.getElementById("kpi-max").innerText = "0.0";
      document.getElementById("kpi-pass").innerText = "0%";
      return;
    }}

    const notas = data.map(d => parseFloat(d.nota));
    const suma = notas.reduce((a, b) => a + b, 0);
    const avg = (suma / data.length).toFixed(1);
    const max = Math.max(...notas).toFixed(1);
    const aprobados = notas.filter(n => n >= 6.0).length;
    const passRate = Math.round((aprobados / data.length) * 100);

    document.getElementById("kpi-avg").innerText = avg;
    document.getElementById("kpi-max").innerText = max;
    document.getElementById("kpi-pass").innerText = `${{passRate}}%`;
  }}

  function renderizarTabla(data) {{
    const tbody = document.getElementById("alumnos-tbody");
    if (data.length === 0) {{
      tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 34px;">Aún no hay evaluaciones entregadas.</td></tr>`;
      return;
    }}

    const sorted = [...data].sort((a, b) => b.nota - a.nota);

    tbody.innerHTML = sorted.map((item, idx) => {{
      let gradeClass = "grade-high";
      if (item.nota < 6.0) gradeClass = "grade-low";
      else if (item.nota < 8.0) gradeClass = "grade-med";

      return `
        <tr>
          <td style="font-weight: 800; color: var(--text-muted);">${{idx + 1}}</td>
          <td style="font-weight: 700; color: #1a202c;">${{item.nombre}}</td>
          <td><span style="font-family: 'JetBrains Mono', monospace; background: #e2e6ef; padding: 4px 10px; border-radius: 8px; font-weight: 600;">${{item.carne}}</span></td>
          <td><span class="badge-grade ${{gradeClass}}">${{item.nota.toFixed(1)}} / 10</span></td>
          <td style="font-weight: 600;">${{item.aciertos}} / ${{item.total_preguntas}}</td>
          <td style="font-weight: 700; color: var(--primary-color);">${{item.porcentaje}}%</td>
          <td style="color: var(--text-muted);">${{item.tiempo}}</td>
          <td style="font-size: 0.85rem; color: var(--text-muted);">${{item.fecha_hora}}</td>
          <td style="display: flex; gap: 8px; align-items: center;">
            <button class="btn btn-soft" style="padding: 6px 12px; font-size: 0.82rem;" onclick="verDetalle('${{item.carne}}')">
              👁️ Ver
            </button>
            <button class="btn btn-action-unlock" title="Permitir que este alumno vuelva a hacer el examen" onclick="desbloquearAlumno('${{item.carne}}', '${{item.nombre}}')">
              🔓 Reintento
            </button>
          </td>
        </tr>
      `;
    }}).join("");
  }}

  function verDetalle(carne) {{
    const alumno = cachedResultados.find(r => r.carne === carne);
    if (!alumno) return;

    document.getElementById("modal-student-name").innerText = `${{alumno.nombre}} — Nota: ${{alumno.nota}} / 10`;
    document.getElementById("modal-student-sub").innerText = `Carné: ${{alumno.carne}} • Aciertos: ${{alumno.aciertos}} / ${{alumno.total_preguntas}} (${{alumno.porcentaje}}%) • Tiempo: ${{alumno.tiempo}}`;

    const list = document.getElementById("modal-questions-list");
    list.innerHTML = (alumno.respuestas || []).map((ans, idx) => `
      <div class="detail-item ${{ans.isCorrect ? 'pass' : 'fail'}}">
        <div style="font-weight: 700; margin-bottom: 6px; color: #1a202c;">
          ${{idx + 1}}. ${{ans.enunciado}}
        </div>
        <div style="display: flex; gap: 16px; font-size: 0.88rem; margin-top: 8px; flex-wrap: wrap;">
          <span>Respuesta Alumno: <b style="color: ${{ans.isCorrect ? 'var(--success)' : 'var(--danger)'}}">${{ans.seleccionada}}</b></span>
          <span>Correcta: <b style="color: var(--success);">${{ans.correcta}}</b></span>
          <span style="font-weight: 700; color: ${{ans.isCorrect ? 'var(--success)' : 'var(--danger)'}};">${{ans.isCorrect ? '✓ Correcto' : '✗ Incorrecto'}}</span>
        </div>
      </div>
    `).join("");

    document.getElementById("detail-modal").style.display = "flex";
  }}

  function cerrarModal() {{
    document.getElementById("detail-modal").style.display = "none";
  }}

  function desbloquearAlumno(carne, nombre) {{
    if (!confirm(`¿Deseas permitir un reintento al estudiante ${{nombre}} (${{carne}})?\\n\\nSu nota actual será eliminada del servidor para que pueda ingresar nuevamente desde el inicio.`)) return;

    fetch(`/api/permitir_reintento?carne=${{encodeURIComponent(carne)}}&pin=${{sessionPin}}`, {{ method: "POST" }})
      .then(res => res.json())
      .then(data => {{
        if (data.status === "unlocked") {{
          alert(`✓ Reintento habilitado para ${{nombre}}. Ahora puede ingresar nuevamente su carné y realizar el examen.`);
          cargarResultados();
        }}
      }})
      .catch(err => alert("Error al autorizar reintento: " + err));
  }}

  function limpiarResultados() {{
    if (!confirm("¿Estás seguro de que deseas reiniciar todos los registros de evaluación? Esta acción no se puede deshacer.")) return;
    fetch(`/api/limpiar_resultados?pin=${{sessionPin}}`, {{ method: "POST" }})
      .then(res => res.json())
      .then(() => cargarResultados())
      .catch(err => alert("Error al limpiar: " + err));
  }}
</script>

</body>
</html>
'''

# ==============================================================================
# HTTP REQUEST HANDLER
# ==============================================================================
class EvaluacionHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        if "/api/resultados" in self.path or "/api/estado_alumno" in self.path:
            return
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_ALUMNO.encode("utf-8"))

        elif path == "/docente":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DOCENTE.encode("utf-8"))

        elif path == "/api/estado_alumno":
            carne = query.get("carne", [""])[0].strip().upper()
            resultados = leer_resultados()
            alumno = next((r for r in resultados if r.get("carne", "").upper() == carne), None)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            if alumno:
                resp = {"entregado": True, "resultado": alumno}
            else:
                resp = {"entregado": False}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/resultados":
            pin = query.get("pin", [""])[0]
            if pin != PIN_DOCENTE:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "No autorizado"}')
                return

            data = leer_resultados()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/exportar_csv":
            pin = query.get("pin", [""])[0]
            if pin != PIN_DOCENTE:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'No autorizado')
                return

            data = leer_resultados()
            output = io.StringIO()
            output.write('\ufeff')
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Posición", "Nombre Alumno", "Carné", "Nota Final (0-10)", "Aciertos", "Fallos", "Precisión (%)", "Tiempo", "Fecha y Hora"])
            
            sorted_data = sorted(data, key=lambda x: x.get("nota", 0), reverse=True)
            for i, r in enumerate(sorted_data):
                writer.writerow([
                    i + 1,
                    r.get("nombre", ""),
                    r.get("carne", ""),
                    f"{r.get('nota', 0):.1f}",
                    r.get("aciertos", 0),
                    r.get("fallos", 0),
                    f"{r.get('porcentaje', 0)}%",
                    r.get("tiempo", ""),
                    r.get("fecha_hora", "")
                ])

            csv_bytes = output.getvalue().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="Notas_Evaluacion_SQL.csv"')
            self.end_headers()
            self.wfile.write(csv_bytes)

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/guardar_resultado":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                total = guardar_resultado(data)
                print(f" [ENTREGA REGISTRADA] {data.get('nombre')} ({data.get('carne')}) -> Nota: {data.get('nota')}/10 | Total entregas: {total}")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode("utf-8"))

        elif path == "/api/permitir_reintento":
            pin = query.get("pin", [""])[0]
            carne = query.get("carne", [""])[0].strip().upper()
            if pin != PIN_DOCENTE:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "No autorizado"}')
                return

            eliminado = eliminar_resultado_alumno(carne)
            print(f" [DOCENTE HABILITÓ REINTENTO] Carné: {carne}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "unlocked"}')

        elif path == "/api/limpiar_resultados":
            pin = query.get("pin", [""])[0]
            if pin != PIN_DOCENTE:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'{"error": "No autorizado"}')
                return

            with open(RESULTADOS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

            print(" [AVISO] Se han reiniciado todos los resultados de evaluación.")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "cleared"}')

        else:
            self.send_response(404)
            self.end_headers()

def main():
    ip = get_local_ip()
    server = ServerClass(("0.0.0.0", PORT), EvaluacionHandler)
    
    print("=" * 74)
    print("  AUDITORÍA DE SISTEMAS — SERVIDOR DE EVALUACIÓN INTERACTIVA (MySQL)")
    print("  Diseño Neumórfico (Soft UI) + Anti-Trampas + Auto-Reanudación")
    print("=" * 74)
    print(f"\n  📡 ENLACE PARA QUE LOS ALUMNOS ENTREN AL EXAMEN:")
    print(f"     http://{ip}:{PORT}/")
    print(f"     (o http://localhost:{PORT}/ si pruebas en esta misma PC)")
    print(f"\n  🔐 PANEL DE CONTROL DEL DOCENTE (Resultados en Vivo):")
    print(f"     http://localhost:{PORT}/docente")
    print(f"     PIN de Acceso: {PIN_DOCENTE} (Visible, sin máscara)")
    print(f"\n  📁 Los resultados se guardan automáticamente en:")
    print(f"     {RESULTADOS_FILE}")
    print("\n  Presiona Ctrl + C en esta ventana para detener el servidor.")
    print("=" * 74)
    print("  Esperando conexiones de alumnos...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido por el docente.")
        server.server_close()

if __name__ == "__main__":
    main()
