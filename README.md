# Django TCP Demo

This repository contains a small Django project that exposes a REST API and an extra endpoint for uploading images encoded in Base64. Uploaded images are resized, converted to a simplified RGB map and the data is transmitted over a TCP socket.

## Features

- CRUD API for **Hero** objects.
- CRUD API for **Image** objects.
- `/login/` endpoint that accepts a JSON payload with a Base64 encoded image and sends a color map to a remote TCP server.

## Requirements

- Python 3.6+
- Django 2.2
- Django REST framework
- Pillow

Install the dependencies with `pip`:

```bash
pip install django==2.2 djangorestframework pillow
```

## Setup

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```

The project uses SQLite by default (`db.sqlite3`).

## API Overview

The API routes are registered in `myapi/urls.py` and `mysite/urls.py`:

```python
router.register(r'heroes', views.HeroViewSet)
router.register(r'images', views.ImagenViewSet)
```

- `GET /heroes/` – list heroes
- `POST /heroes/` – create a hero
- `GET /images/` – list images
- `POST /images/` – create an image

The `login/` endpoint is defined in `mysite/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapi.urls')),
    path('login/', login),
]
```

Send a POST request with a JSON body containing a `base64` field:

```bash
curl -X POST http://localhost:8000/login/ \
    -H "Content-Type: application/json" \
    -d '{"base64": "<base64-image>"}'
```

The uploaded image is resized to 240×320 pixels and mapped to letters `R`, `G`, or `B` based on the dominant color. The resulting data is written to `rgb.txt` and `listaRGB.txt` and each entry is sent over TCP to `192.168.1.13:5005`.

Key parts of the implementation can be found in `myapi/views.py`:

```python
width = 240
height = 320
im1 = PIL.Image.open(BytesIO(base64.b64decode(stringImagen)))
im2 = im1.resize((width, height), PIL.Image.NEAREST)
...
TCP_IP = '192.168.1.13'
TCP_PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

## License

This project was published as an example and does not include a specific license.

## Author

Luis Vargas
