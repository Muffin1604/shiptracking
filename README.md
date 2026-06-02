# Ship Tracking Backend

Django REST Framework API that fetches vessel data from the [Data Docked](https://datadocked.com) API, stores it in SQLite, and exposes authenticated JSON endpoints for ship info, live tracking, and weather.

## Features

- **JWT authentication** — register, login, token refresh (email-based users)
- **Ship info** — full vessel profile (specs, engine, management, etc.)
- **Ship tracking** — location snapshots with history
- **Weather** — temperature, wind, and wave data per vessel
- **Sync** — one-call endpoint to refresh info, location, and weather

## Project structure

```
ship-tracking/
├── docked/                      # Sample API scripts & response files
├── shiptracking/                # Django project (settings, urls)
├── users/                       # Custom User model + auth API
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── vessels/                     # Vessel models + Docked sync API
│   ├── models.py
│   ├── services/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── .env
```

## Requirements

- Python 3.12+
- Data Docked API key

## Setup

1. **Clone and enter the project**

   ```bash
   cd ship-tracking
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   DATA_DOCKED_API_KEY=your_api_key_here
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

## Authentication (JWT)

All vessel endpoints require a valid JWT access token in the header:

```http
Authorization: Bearer <access_token>
```

### Register

```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

### Login (obtain tokens)

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Refresh access token

```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

### Current user

```http
GET /api/auth/me/
Authorization: Bearer <access_token>
```

### Change password (logged in)

```http
POST /api/auth/password/change/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "currentpass",
  "new_password": "newsecurepass"
}
```

### Forgot password

Sends a reset link to the user's email. The link points to your frontend (`FRONTEND_RESET_PASSWORD_URL`) with `uid` and `token` query params.

```http
POST /api/auth/password/forgot/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

In development (`DEBUG=True`), the response also includes `resetUrl`, `uid`, and `token` for testing. Emails are printed to the console when using the default console email backend.

### Reset password (with token from email)

```http
POST /api/auth/password/reset/
Content-Type: application/json

{
  "uid": "<uid from reset link>",
  "token": "<token from reset link>",
  "new_password": "newsecurepass"
}
```

Optional email settings in `.env` for production:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your_smtp_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
FRONTEND_RESET_PASSWORD_URL=https://yourapp.com/reset-password
```

## Vessel API reference

Replace `{imo_or_mmsi}` with a vessel IMO or MMSI (e.g. `9218301`). All routes require JWT authentication.

### List vessels

```http
GET /api/vessels/
```

### Ship info

```http
POST /api/vessels/{imo_or_mmsi}/info/   # Fetch from Docked and store
GET  /api/vessels/{imo_or_mmsi}/info/   # Return stored info
```

### Ship tracking

```http
POST /api/vessels/{imo_or_mmsi}/track/   # Fetch location and save snapshot
GET  /api/vessels/{imo_or_mmsi}/track/   # Latest + history
GET  /api/vessels/{imo_or_mmsi}/track/?limit=10
```

### Weather

```http
POST /api/vessels/{imo_or_mmsi}/weather/   # Fetch and store
GET  /api/vessels/{imo_or_mmsi}/weather/   # Latest reading
```

### Sync all

```http
POST /api/vessels/{imo_or_mmsi}/sync/
```

## Example usage

Register and log in:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo12345"}'

curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo12345"}'
```

Sync a vessel (use the `access` token from login):

```bash
curl -X POST http://127.0.0.1:8000/api/vessels/9218301/sync/ \
  -H "Authorization: Bearer <access_token>"
```

## Database models

| Model | App | Description |
|-------|-----|-------------|
| `User` | `users` | Email-based user (JWT auth) |
| `VesselInfo` | `vessels` | Vessel profile (upserted on sync) |
| `VesselLocation` | `vessels` | Position snapshot per track sync |
| `VesselWeather` | `vessels` | Weather reading per weather sync |

## Django admin

```bash
python manage.py createsuperuser
```

Admin: `http://127.0.0.1:8000/admin/` (use email as login)

## Error responses

DRF returns standard error shapes, e.g.:

```json
{ "detail": "Authentication credentials were not provided." }
```

```json
{ "detail": "Vessel not found. Sync info first." }
```

Common status codes: `401` (missing/invalid JWT), `404` (not found), `502` (Docked API error).
