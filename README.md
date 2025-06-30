# Telesalud U.A.P.

Aplicación web para médicos que atienden por telesalud, construida con Flask. Permite login seguro, gestión de historias clínicas con generación de PDF, y consultas por fecha.

## 🚀 Despliegue en Render

1. Crea una cuenta en https://render.com
2. Crea un nuevo Web Service desde tu repositorio de GitHub.
3. Usa los siguientes comandos:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## 🌐 Dominio personalizado

Puedes conectar el dominio `telemedicinauap.com.bo` desde Render siguiendo:
- Settings → Custom Domains → Agrega tu dominio y sigue pasos para verificar DNS.

## 🗂 Estructura básica

- `app.py`: Aplicación principal Flask
- `templates/`: HTMLs
- `static/`: Archivos estáticos (CSS, imágenes, etc)
- `medica.db`: Base de datos SQLite
- `render.yaml`: Configuración automática para Render
