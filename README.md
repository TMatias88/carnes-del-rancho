# Carnes del Rancho (Starter Django)

Proyecto base Django con catálogo, carrito de compras (sesión) y checkout con métodos: SINPE/Transferencia y Contraentrega.
**Base de datos por defecto: SQLite (rápido para desarrollar).**

## Requisitos (macOS)
- Python 3.10+ (sugerido instalar con Homebrew)
- (Opcional) PostgreSQL si vas a migrar a producción

## Pasos rápidos
```bash
# 1) Crear carpeta de trabajo y entrar
cd "/mnt/data/carnes_del_rancho"

# 2) Crear y activar entorno
python3 -m venv .venv
source .venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt

# 4) Migrar DB y crear superusuario
python manage.py migrate
python manage.py createsuperuser

# 5) Ejecutar servidor
python manage.py runserver
```

Abre http://127.0.0.1:8000/ para ver la web.
Entra a http://127.0.0.1:8000/admin/ para crear **Categorías** y **Productos** con imágenes.

## Migrar a PostgreSQL (después)
- Cambia `DATABASES` en `settings.py` al bloque Postgres (descomentando y ajustando credenciales).
- Exporta datos si estabas en SQLite:
  ```bash
  python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > data.json
  ```
- Cambia a Postgres y:
  ```bash
  python manage.py migrate
  python manage.py loaddata data.json
  ```

## Estructura
- `catalog`: modelos y vistas de productos/categorías
- `cart`: lógica de carrito en sesión
- `orders`: checkout, órdenes y admin
- `templates`: HTML base (`home.html`, `cart.html`, `checkout.html`, `order_thanks.html`)
- `static`: CSS (puedes pegar tu CSS y JS actual)
- `media`: se guardan las imágenes subidas (productos, comprobantes)

## Notas
- Este starter está listo para que pegues tu diseño (HTML/CSS/JS) en `templates` y `static`.
- Para producción añade WhiteNoise o CDN para estáticos, y configura DEBUG=False y ALLOWED_HOSTS.
# carnes-del-rancho
