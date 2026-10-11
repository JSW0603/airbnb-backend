# Airbnb Backend

REST API backend for an Airbnb-style accommodation platform, built with Django and Django REST Framework. 🚧 Actively developed — new endpoints and tests are added regularly.

## Tech Stack

- **Python** 3.10+
- **Django** 5.2
- **Django REST Framework** 3.17 (class-based `APIView`s)
- **Poetry** for dependency management
- **SQLite** (dev) — PostgreSQL planned

## Features

### Users (`/api/v1/users/`)
- User registration and listing
- Log in / log out (session-based)
- View and update own profile
- Change password
- Public user profile by username

### In progress
- Experiences API (CRUD completed, being extended)
- Rooms, categories, wishlists, medias apps — models in place, endpoints being built

## Project Structure

```
.
├── config/          # Django settings, root URLs
├── users/           # Auth + profiles
├── rooms/           # Property listings
├── experiences/     # Experience listings
├── bookings/        # Reservations
├── reviews/         # Ratings & reviews
├── wishlists/       # Saved listings
├── medias/          # File uploads (Pillow)
├── categories/      # Listing categories
├── directmessage/   # Host-guest messaging
├── common/          # Shared base models
└── manage.py
```

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/JSW0603/airbnb-backend.git
cd airbnb-backend

# 2. Install dependencies (Poetry)
poetry install
poetry shell

# 3. Apply migrations
python manage.py migrate

# 4. Create an admin user
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000/admin/ or try the API at http://127.0.0.1:8000/api/v1/.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET / POST | `/api/v1/users/` | List users / register |
| GET / PUT | `/api/v1/users/me` | Own profile |
| PUT | `/api/v1/users/change-password` | Change password |
| POST | `/api/v1/users/login` | Log in |
| POST | `/api/v1/users/logout` | Log out |
| GET | `/api/v1/users/@<username>` | Public profile |
| … | `/api/v1/rooms/`, `/api/v1/experiences/`, … | Other resources (in progress) |

## Roadmap

- [ ] pytest test coverage for users API
- [ ] JWT authentication (djangorestframework-simplejwt)
- [ ] PostgreSQL + Docker setup
- [ ] API documentation (drf-spectacular)

## License

MIT
