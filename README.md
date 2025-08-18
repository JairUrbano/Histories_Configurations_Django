# [Histories Configurations] - README de Migración

Este documento detalla la migración de un proyecto desarrollado en **PHP/Laravel** a **Python/Django**. Sirve como guía de instalación, ejecución y referencia técnica sobre la nueva arquitectura.

## 1. Visión General del Proyecto

Este sistema gestiona tipos de documento, precios e historiales para una plataforma interna de facturación. Su objetivo es centralizar la configuración maestra de la aplicación.

---

## 2. Detalles de la Migración

### 2.1. Comparativa de Stacks Tecnológicos

| Característica | Pila Tecnológica Anterior (Legacy) | Pila Tecnológica Actual (Nueva) |
| :--------------- | :--------------------------------- | :------------------------------ |
| **Lenguaje**     | PHP 8.x                            | Python 3.9+                     |
| **Framework**    | Laravel 9.x                        | Django 4.x                      |
| **ORM**          | Eloquent ORM                       | Django ORM                      |
| **Base de Datos**| MySQL / PostgreSQL                 | PostgreSQL / SQLite (desarrollo) |
| **Servidor**     | Apache / Nginx                     | Gunicorn / Nginx                |

### 2.2. Mapeo de Estructuras: Laravel a Django

La siguiente tabla muestra la correspondencia entre los componentes del proyecto original y su equivalente en la nueva estructura Django.

| Componente en Laravel (Directorio Original) | Equivalente en Django (App/Módulo) | Notas de Migración |
| :------------------------------------------ | :---------------------------------- | :----------------- |
| `modelo/`                                   | `core/models.py`                    | Los modelos Eloquent fueron reescritos como modelos de Django, con campos explícitos. |
| `views/` (Controladores)                    | `core/views.py`                     | La lógica de los controladores ahora reside en las vistas de Django (basadas en funciones o clases). |
| `forms/` (Form Requests)                    | `core/forms.py`                     | La validación se gestiona con `django.forms.ModelForm` o `django.forms.Form`. |
| `service/`                                  | `core/services.py` (Convención)     | La lógica de negocio se encapsuló en funciones para mantener las vistas limpias. |
| `migrations/`                               | `core/migrations/` (Autogenerado)   | Las migraciones se regeneraron con los comandos de Django a partir de los nuevos modelos. |
| `routes/web.php`                            | `mi_proyecto/urls.py` y `core/urls.py` | El enrutamiento ahora es modular y se define explícitamente en los archivos `urls.py`. |

---

## 3. Guía de Instalación y Ejecución

### 3.1. Requisitos Previos

*   Python 3.9 o superior
*   Pip (gestor de paquetes de Python)
*   Git

### 3.2. Configuración del Entorno Local

1.  **Clonar el repositorio:**
    ```bash
    git clone [URL de tu repositorio]
    cd [nombre-de-la-carpeta-del-proyecto]
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    *(Asegúrate de haber creado el archivo `requirements.txt` con `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno:**
    Copia el archivo de ejemplo `.env.example` a uno nuevo llamado `.env` y rellena las variables necesarias (SECRET_KEY, DEBUG, configuración de la base de datos, etc.).
    ```bash
    cp .env.example .env
    ```

### 3.3. Base de Datos

Para inicializar la base de datos, ejecuta los siguientes comandos:

1.  **Crear las migraciones:**
    ```bash
    python manage.py makemigrations
    ```

2.  **Aplicar las migraciones:**
    ```bash
    python manage.py migrate
    ```

### 3.4. Ejecutar el Servidor de Desarrollo

Una vez configurado todo, inicia el servidor local:
```bash
python manage.py runserver


>>>>>>> f1bed002e6a21ce8ff5dc2ce34b68e11405cea34
