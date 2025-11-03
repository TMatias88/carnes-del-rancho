from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# === Paths / ENV ==============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# === Core ====================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    ".onrender.com,localhost,127.0.0.1"
).split(",")


LANGUAGE_CODE = "es"
TIME_ZONE = "America/Costa_Rica"
USE_I18N = True
USE_TZ = True

# === Apps ====================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # apps del proyecto
    "catalog",
    "cart",
    "orders",
    "pages",
    "payments",
]

# === Middleware ===============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
ROOT_URLCONF = "carnes_del_rancho.urls"

# === Templates ================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "carnes_del_rancho.wsgi.application"

# === Database (PostgreSQL) ====================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "carnes_rancho"),
        "USER": os.getenv("DB_USER", "CarnesDelRancho"),
        "PASSWORD": os.getenv("DB_PASSWORD", "tati"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5433"),
    }
}

# === Password Validation ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Static & Media ===========================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# === Email (SMTP real; cae a consola si faltan credenciales) ==================
import os

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.me.com")  # iCloud por defecto
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"  # normalmente False
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "30"))

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "tatianamatias@icloud.com")  # remitente
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")  # contraseña de aplicación

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX", "[Carnes del Rancho] ")

# Destinatarios para el formulario (coma-separados)
_contact_list = os.getenv("CONTACT_RECIPIENTS", "tatianamatias@icloud.com")
CONTACT_RECIPIENTS = [x.strip() for x in _contact_list.split(",") if x.strip()]

# Usa SMTP solo si hay password; si no, imprime en consola (útil en dev)
if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
