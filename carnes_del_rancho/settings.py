from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# === Paths / ENV ==========================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# === Core =================================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "carnes-del-rancho.onrender.com",
    "localhost",
    "127.0.0.1",
]

# === CSRF =================================================================================
CSRF_TRUSTED_ORIGINS = [
    "https://carnes-del-rancho.onrender.com",
]

_extra_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if _extra_csrf.strip():
    CSRF_TRUSTED_ORIGINS += [
        x.strip() for x in _extra_csrf.split(",") if x.strip()
    ]

# === Configuración regional ================================================================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Costa_Rica"
USE_I18N = True
USE_TZ = True

# === Apps ==================================================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    # Apps del proyecto
    "catalog",
    "cart",
    "orders",
    "pages",
    "payments",
]

# === Middleware ============================================================================
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

ROOT_URLCONF = "carnes_del_rancho.urls"

# === Templates =============================================================================
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

# === WSGI ==================================================================================
WSGI_APPLICATION = "carnes_del_rancho.wsgi.application"

# === DATABASE (Render) =====================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "")

DATABASES = {}
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=False,     # Render NO usa SSL obligatorio
    )
else:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "local_db"),
        "USER": os.getenv("DB_USER", "local_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "local_pass"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }

# === Password Validation ====================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === STATIC (WhiteNoise – Render) ============================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# === MEDIA (local y Render – sin Spaces) =====================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# === Email ===================================================================================
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.me.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "30"))

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

CONTACT_RECIPIENTS = [
    x.strip()
    for x in os.getenv("CONTACT_RECIPIENTS", EMAIL_HOST_USER).split(",")
    if x.strip()
]

if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# === Logging ==================================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
}
