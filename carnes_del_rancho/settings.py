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

ALLOWED_HOSTS = [
    "walrus-app-uvvxz.ondigitalocean.app",
    "localhost",
    "127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = [
    "https://walrus-app-uvvxz.ondigitalocean.app"
]

_extra_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if _extra_csrf.strip():
    CSRF_TRUSTED_ORIGINS += [x.strip() for x in _extra_csrf.split(",") if x.strip()]

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

    # AWS S3 / Spaces
    "storages",
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

TEMPLATES[0]["OPTIONS"].setdefault("builtins", [])
TEMPLATES[0]["OPTIONS"].setdefault("libraries", {})

if "orders.templatetags.form_extras" not in TEMPLATES[0]["OPTIONS"]["builtins"]:
    TEMPLATES[0]["OPTIONS"]["builtins"].append("orders.templatetags.form_extras")

TEMPLATES[0]["OPTIONS"]["libraries"]["form_extras"] = "orders.templatetags.form_extras"

WSGI_APPLICATION = "carnes_del_rancho.wsgi.application"

# === Database (PostgreSQL) ====================================================
DATABASES = {}
_database_url = os.getenv("DATABASE_URL", "").strip()

if _database_url:
    DATABASES["default"] = dj_database_url.config(
        default=_database_url,
        conn_max_age=600,
        ssl_require=True,
    )
else:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "carnes_rancho"),
        "USER": os.getenv("DB_USER", "CarnesDelRancho"),
        "PASSWORD": os.getenv("DB_PASSWORD", "tati"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5433"),
    }

# === Password Validation ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Static ===================================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# === DEBUG ===============================================================
DEBUG = False

# === Media (Local vs DigitalOcean Spaces) ================================
MEDIA_URL = "https://carnes-del-rancho-media.nyc3.digitaloceanspaces.com/"
MEDIA_ROOT = BASE_DIR / "media"

if not DEBUG:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_ACCESS_KEY_ID = os.getenv("SPACES_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("SPACES_SECRET")
    AWS_STORAGE_BUCKET_NAME = os.getenv("SPACES_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("SPACES_ENDPOINT")

    AWS_S3_REGION_NAME = "nyc3"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_DEFAULT_ACL = "public-read"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# === Email ====================================================================
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.me.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "30"))

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "tatianamatias@icloud.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

_contact_list = os.getenv("CONTACT_RECIPIENTS", "tatianamatias@icloud.com")
CONTACT_RECIPIENTS = [x.strip() for x in _contact_list.split(",") if x.strip()]

if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# === Logging ==================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
}
