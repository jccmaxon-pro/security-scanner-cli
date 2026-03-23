# Security Scanner CLI

Herramienta básica de auditoría de red desarrollada en Python para escanear puertos, identificar servicios comunes, capturar banners básicos y generar informes en CSV y HTML.

## Descripción

Este proyecto consiste en un escáner de puertos por línea de comandos orientado a entornos de laboratorio, pruebas locales y auditorías autorizadas. Permite analizar un objetivo (IP o dominio), detectar puertos abiertos o cerrados, asociar servicios típicos, intentar capturar banners simples y exportar los resultados en formatos reutilizables.

El proyecto está diseñado como una herramienta de portfolio para demostrar conocimientos básicos de redes, sockets, automatización y reporting técnico.

## Características principales

- Escaneo de puertos TCP
- Escaneo de puertos comunes por defecto
- Escaneo de una lista manual de puertos
- Escaneo por rango de puertos
- Detección de estado abierto/cerrado
- Asociación de servicios comunes por puerto
- Captura básica de banners
- Informe CSV
- Informe HTML visual
- Tarjetas resumen en HTML
- Timestamp y duración del escaneo
- Uso desde línea de comandos (CLI)

## Tecnologías utilizadas

- Python
- Socket
- Argparse
- CSV
- HTML
- Pathlib

## Estructura del proyecto

```bash
security-scanner/
│
├── app/
│   ├── main.py
│   ├── scanner.py
│   └── exporter.py
│
├── output/
├── requirements.txt
└── README.md


## Instalación

Clona el repositorio y crea un entorno virtual:

git clone <TU_REPO_URL>
cd security-scanner
python3 -m venv venv
source venv/bin/activate

Este proyecto no requiere dependencias externas adicionales para la versión actual, pero puedes dejar el entorno preparado igualmente.


## Uso

1. Escaneo básico con puertos por defecto
python3 -m app.main --target 127.0.0.1

2. Escaneo de puertos concretos
python3 -m app.main --target 127.0.0.1 --ports 22 80 443

3. Escaneo por rango
python3 -m app.main --target 127.0.0.1 --range 20 100

4. Nombre personalizado de salida
python3 -m app.main --target 127.0.0.1 --range 20 100 --output-name scan_local

Esto generará:

output/scan_local.csv
output/scan_local.html


5. Ajustar timeout
python3 -m app.main --target 127.0.0.1 --range 1 1024 --timeout 0.5


## Salida generada

La herramienta genera dos tipos de informe:

- CSV

Contiene:

target
port
status
service
banner

- HTML

Incluye:

objetivo analizado
fecha y hora
duración del escaneo
tarjetas resumen
tabla detallada de puertos y banners
Servicios comunes detectados

Actualmente la herramienta asocia estos puertos con servicios frecuentes:

21 → FTP
22 → SSH
23 → Telnet
25 → SMTP
53 → DNS
80 → HTTP
110 → POP3
143 → IMAP
443 → HTTPS
3306 → MySQL
3389 → RDP
5432 → PostgreSQL
6379 → Redis
8080 → HTTP-Alt

- Funcionalidades implementadas

Escaneo TCP básico con sockets
Resolución de estado por puerto
Captura de banners simples en algunos servicios
Informes técnicos reutilizables
Salida estructurada para reporting
HTML visual con resumen ejecutivo

- Casos de uso

Este proyecto puede adaptarse para:

 - auditorías básicas autorizadas
 - inventario rápido de servicios
 - laboratorios de redes
 - comprobaciones internas
 - formación en ciberseguridad básica
 - automatización de revisiones técnicas

- Advertencia

Esta herramienta debe utilizarse únicamente sobre:

- sistemas propios
- entornos de laboratorio
- objetivos expresamente autorizados

No debe utilizarse sobre infraestructuras de terceros sin permiso.

## Mejoras futuras

- resolución de IP y hostname en el informe
- escaneo multi-hilo para mayor velocidad
- exportación a JSON
- detección más avanzada de banners
- interfaz web simple
- integración con base de datos
- soporte para UDP básico
- clasificación de riesgo por servicio abierto

## Valor del proyecto

Este proyecto demuestra conocimientos prácticos en:

redes
programación con sockets
automatización
generación de informes
diseño de herramientas CLI orientadas a tareas técnicas

## Autor

Proyecto desarrollado por Juan Carrasco como parte de un portfolio orientado a Python, automatización, ciberseguridad básica y trabajos freelance técnicos.