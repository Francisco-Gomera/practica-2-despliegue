# API REST Django - Gestión de Usuarios y Preferencias Musicales

Una API REST construida con Django para gestionar usuarios y sus preferencias musicales, integrada con la API de Spotify.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución con Docker](#ejecución-con-docker)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso de la API](#uso-de-la-api)
- [Endpoints](#endpoints)
- [Modelos de Datos](#modelos-de-datos)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.12+**
- **Docker Desktop** (opcional, método recomendado)
- **pip** (incluido con Python)
- **Git** (opcional, para control de versiones)
- Credenciales de Spotify (ver [Configuración](#configuración))

**Verificar instalación:**
```bash
python --version
pip --version
```

---

## 📦 Instalación

### 1. Clonar o Descargar el Proyecto

```bash
# Si usas Git
git clone https://github.com/Francisco-Gomera/Practica-3.git
cd Practica-3

# O descargar el ZIP y extraer
```

### 2. Crear un Entorno Virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de la línea de comando.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Django 6.0
- httpx (cliente HTTP)
- requests (para Spotify API)
- python-dotenv (variables de entorno)
- Y más...

### 4. Crear Base de Datos

```bash
python manage.py migrate
```

> **Nota:** Si utilizas Docker, este paso no es necesario. Las migraciones se ejecutan automáticamente al iniciar el contenedor.

Este comando crea la base de datos SQLite y todas las tablas necesarias.

### 5. (Opcional) Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para crear un usuario administrador. Después podrás acceder a:
```
http://127.0.0.1:8000/admin/
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto:

```env
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
```

**Obtener credenciales de Spotify:**

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Inicia sesión o crea una cuenta
3. Crea una nueva aplicación
4. Copia `Client ID` y `Client Secret`
5. Pega los valores en `.env`


### Configuración de Django (api_server/settings.py)

Las configuraciones principales ya están listas:

- `DEBUG = True` (cambiar a `False` en producción)
- `INSTALLED_APPS` incluye `users_view` y `preferences_view`
- Base de datos SQLite en `db.sqlite3`
- CORS habilitado para desarrollo

---

## 🐳 Ejecución con Docker

La aplicación puede ejecutarse sin necesidad de instalar Python, crear entornos virtuales o instalar dependencias manualmente.

### Requisitos

* Docker Desktop instalado y en ejecución.

Verificar instalación:

```bash
docker --version
```

### Construir la imagen

Desde la raíz del proyecto:

```bash
docker build -t practica_3 .
```

### Ejecutar el contenedor

```bash
docker run -p 8000:8000 practica_3
```

### Acceder a la API

Una vez iniciado el contenedor, la API estará disponible en:

```text
http://localhost:8000/
```

### Migraciones automáticas

El contenedor ejecuta automáticamente:

```bash
python manage.py migrate
```

antes de iniciar el servidor ASGI con Uvicorn.

Por ello, no es necesario crear manualmente la base de datos SQLite al ejecutar el proyecto mediante Docker.

### Reconstrucción de la imagen

Si se realizan cambios en el código o en las dependencias:

```bash
docker build --no-cache -t practica_3 .
```

### Detener el contenedor

Presiona:

```text
Ctrl + C
```

o, desde otra terminal:

```bash
docker ps
docker stop <container_id>
```

---

## 📁 Estructura del Proyecto

```
Practica 3/
├── api_server/              # Configuración principal de Django
│   ├── settings.py          # Configuración global
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # Configuración WSGI
│   └── asgi.py              # Configuración ASGI utilizada por Uvicorn
├── users_view/              # App para gestión de usuarios
│   ├── models.py            # Modelo User
│   ├── views.py             # Vistas CRUD de usuarios
│   ├── urls.py              # Rutas de usuarios
│   ├── migrations/          # Migraciones de base de datos
│   └── admin.py             # Administración de Django
├── preferences_view/        # App para preferencias musicales
│   ├── models.py            # Modelo Preference
│   ├── views.py             # Vistas CRUD de preferencias
│   ├── urls.py              # Rutas de preferencias
│   ├── migrations/          # Migraciones de base de datos
│   └── admin.py             # Administración de Django
├── services/                # Servicios externos
│   └── spotifyservices.py   # Integración con Spotify API
├── Dockerfile               # Configuración de la imagen Docker
├── .dockerignore            # Archivos excluidos del contexto Docker
├── requirements.txt         # Dependencias del proyecto
├── manage.py                # Utilidad de administración de Django
├── .env                     # Variables de entorno (no compartir)
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Documentación del proyecto
```

---

## 🚀 Uso de la API

### Usar la API

Puedes usar:
- **Postman** (interfaz gráfica)
- **cURL** (línea de comandos)
- **Thunder Client** (VS Code)
- **Insomnia** (cliente REST)

Ejemplos con **cURL**:

```bash
# Crear usuario
curl -X POST http://127.0.0.1:8000/users/crear/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan"}'

# Obtener usuarios
curl http://127.0.0.1:8000/users/leer/

# Crear preferencia
curl -X POST http://127.0.0.1:8000/preferences/crear/1/ \
  -H "Content-Type: application/json" \
  -d '{"song": "Bohemian Rhapsody", "artist": "Queen"}'

# Obtener preferencias de usuario
curl http://127.0.0.1:8000/preferences/leer/1/
```

---

## 📡 Endpoints

### Usuarios (`/users/`)

| Método | Endpoint | Descripción | Body |
|--------|----------|-------------|------|
| POST | `/users/crear/` | Crear usuario | `{"name": "nombre"}` |
| GET | `/users/leer/` | Obtener todos los usuarios | - |
| PUT | `/users/actualizar/<id>/` | Actualizar usuario | `{"name": "nuevo_nombre"}` |
| DELETE | `/users/eliminar/<id>/` | Eliminar usuario | - |

**Ejemplo de respuesta GET:**
```json
{
  "success": true,
  "message": "usuarios obtenidos exitosamente",
  "total": 2,
  "data": [
    {"id": 1, "name": "Juan"},
    {"id": 2, "name": "María"}
  ]
}
```

### Preferencias (`/preferences/`)

| Método | Endpoint | Descripción | Body |
|--------|----------|-------------|------|
| POST | `/preferences/crear/<user_id>/` | Crear preferencia | `{"song": "...", "artist": "..."}` |
| GET | `/preferences/leer/<user_id>/` | Obtener preferencias del usuario | - |
| PUT | `/preferences/actualizar/<id>/` | Actualizar preferencia | `{"song": "...", "artist": "..."}` |
| DELETE | `/preferences/eliminar/<id>/` | Eliminar preferencia | - |

**Ejemplo de respuesta POST:**
```json
{
  "success": true,
  "message": "preferencia creada exitosamente"
}
```

**Nota:** Al eliminar un usuario, sus preferencias se eliminan automáticamente (ON DELETE CASCADE).

---

## 🗄️ Modelos de Datos

### User (usuarios_view.models)

```python
class User(models.Model):
    id          # AutoField (Primary Key)
    name        # CharField(max_length=100)
```

**Tabla:** `users_view_user`

### Preference (preferences_view.models)

```python
class Preference(models.Model):
    id          # AutoField (Primary Key)
    user        # ForeignKey(User, on_delete=CASCADE)  # Vinculado a User
    song        # CharField(max_length=100)
    artist      # CharField(max_length=100)
```

**Tabla:** `preferencias`

**Relación:** Cuando eliminas un usuario, todas sus preferencias se eliminan automáticamente.

---

## 🔍 Ejemplos Prácticos

### 1. Crear un Usuario

```bash
curl -X POST http://127.0.0.1:8000/users/crear/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos"}'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "usuario creado exitosamente"
}
```

### 2. Obtener Todos los Usuarios

```bash
curl http://127.0.0.1:8000/users/leer/
```

**Respuesta:**
```json
{
  "success": true,
  "message": "usuarios obtenidos exitosamente",
  "total": 3,
  "data": [
    {"id": 1, "name": "Juan"},
    {"id": 2, "name": "María"},
    {"id": 3, "name": "Carlos"}
  ]
}
```

### 3. Crear una Preferencia para el Usuario 1

```bash
curl -X POST http://127.0.0.1:8000/preferences/crear/1/ \
  -H "Content-Type: application/json" \
  -d '{"song": "Shape of You", "artist": "Ed Sheeran"}'
```

### 4. Obtener Preferencias del Usuario 1

```bash
curl http://127.0.0.1:8000/preferences/leer/1/
```

**Respuesta (búsqueda en Spotify):**
```json
{
  "success": true,
  "message": "preferencias del usuario 1 obtenidas",
  "usuario": "Juan",
  "total": 1,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "song": "Shape of You",
      "artist": "Ed Sheeran"
    }
  ],
  "spotify_results": [
    {
      "busqueda_original": "Shape of You - Ed Sheeran",
      "encontrado": true,
      "titulo": "Shape of You",
      "artista": "Ed Sheeran",
      "album": "÷",
      "imagen": "https://...",
      "spotify_url": "https://open.spotify.com/track/...",
      "track_id": "7qiZfU4dY1lsylvNFoO1Z6"
    }
  ]
}
```

---

## 🛠️ Comandos Útiles de Django

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones a la BD
python manage.py migrate

# Acceder a shell interactivo de Django
python manage.py shell

# Ver todas las rutas disponibles
python manage.py show_urls

# Crear superusuario para admin
python manage.py createsuperuser

# Ejecutar tests
python manage.py test
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución:** Asegúrate de tener activado el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Error: "database is locked"

**Solución:** SQLite tiene conflictos de acceso. Reinicia el servidor:
```bash
# 1. Detén el servidor (Ctrl+C)
# 2. Vuelve a ejecutar
python manage.py runserver
```

### Error: "no such table"

**Causa:** Las migraciones no se han aplicado correctamente.

**Solución (ejecución local):**

```bash
python manage.py migrate
```

**Solución (Docker):**

Reconstruir la imagen y volver a ejecutar el contenedor:

```bash
docker build --no-cache -t practica_3 .
docker run -p 8000:8000 practica_3
```

Verificar que los archivos de migración existan dentro de cada aplicación:

```text
users_view/migrations/0001_initial.py
preferences_view/migrations/0001_initial.py
```


### Error: "CSRF token missing"

**Solución:** El token CSRF está deshabilitado con `@csrf_exempt`. En producción, implementar CSRF token correctamente.

### Spotify no devuelve resultados

**Soluciones:**
1. Verificar credenciales en `.env`
2. Revisar que la canción y artista sean correctos
3. Verificar conexión a Internet
4. Ver logs del servidor para errores

---

## 📚 Documentación Adicional

- [Django Docs](https://docs.djangoproject.com/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [httpx Documentation](https://www.python-httpx.org/)

---

## 📝 Licencia

Este proyecto es de uso educativo.

---

## 👤 Autor

Desarrollado por Francisco M. Gomera M. como parte del Máster en Programación Web.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**Última actualización:** 04 de Junio, 2026
