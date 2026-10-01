# SwapEx — Django Backend

REST API for **SwapEx**, a student marketplace where verified students can list, browse, favourite and buy second-hand items. Live at [swapex.art](https://swapex.art).

Built with Django 5.2 and Django REST Framework, using JWT authentication, PostgreSQL, and AWS S3 for media/static files. Deployed on AWS Elastic Beanstalk.

## Features

- **Student accounts** — email-based login with a custom `Student` user model. New sign-ups upload a student ID image and must be approved by an admin before they can log in.
- **JWT auth** — access/refresh tokens via `djangorestframework-simplejwt`.
- **Product listings** — create, edit, search, filter and sort listings with image upload. Edited listings are deactivated until an admin re-approves them.
- **Favourites** — users can save products to a personal favourites list.
- **Wallet** — top up, deduct and check balance; top-ups are recorded as transactions.
- **Sales** — record a purchase, which marks the product as sold and logs a sale transaction.
- **Trust badges** — buyers can award a trust badge to sellers.
- **Admin moderation** — dedicated admin views for pending sign-up requests and pending products, with bulk approve/reject actions.

## Tech stack

| Area | Tools |
|------|-------|
| Framework | Django 5.2, Django REST Framework 3.16 |
| Auth | SimpleJWT |
| Database | PostgreSQL (`psycopg2-binary`) |
| Storage | AWS S3 via `django-storages` + `boto3` (production), local filesystem (development) |
| Filtering | `django-filter` |
| CORS | `django-cors-headers` |
| Hosting | AWS Elastic Beanstalk |

## Project structure

```
.
├── swapex/                 # Project settings, root URLs, WSGI/ASGI, S3 storage backends
├── authentication/         # Student model, sign-up, login, profile, wallet, trust badges
├── products/               # Products, favourites, sale transactions
├── .ebextensions/          # Elastic Beanstalk config (collectstatic, WSGI path)
├── manage.py
└── requirements.txt
```

## Getting started (local development)

### Prerequisites

- Python 3.11+
- PostgreSQL running locally

### Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/1322harshd/SwapEx-DjangoBackend.git
cd SwapEx-DjangoBackend

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Database

When `DB_NAME` is **not** set, the app uses the local database configured at the bottom of the `DATABASES` block in [swapex/settings.py](swapex/settings.py) (database `todoapp_db`, user `postgres` on `localhost:5432`). Either create a matching database or update those values to your own:

```bash
createdb todoapp_db
```

### Run

```bash
export DEBUG=True               # serves uploaded media locally and shows error pages

python manage.py migrate
python manage.py createsuperuser   # prompts for email + password
python manage.py runserver
```

The API is now at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

Uploaded files are stored in `media/` locally. The front end is expected on `http://localhost:5173` (Vite) or `http://localhost:3000`, both already allowed by CORS.

## Environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev key — **always set in production** |
| `DEBUG` | `True` to enable debug mode | `False` |
| `DB_NAME` | Database name. **Setting this switches to production mode** (env-based DB + HTTPS/HSTS settings) | — |
| `DB_USER` / `DB_PASSWORD` / `DB_HOST` | Database credentials | — |
| `DB_PORT` | Database port | `5432` |
| `DB_ENGINE` | Django DB backend | `django.db.backends.postgresql_psycopg2` |
| `AWS_STORAGE_BUCKET_NAME` | Setting this enables S3 storage for static and media files | — |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | AWS credentials | — |
| `AWS_S3_REGION_NAME` | S3 region | `ap-southeast-2` |
| `AWS_S3_CUSTOM_DOMAIN` | Custom domain / CDN for S3 | `<bucket>.s3.<region>.amazonaws.com` |

## API reference

All endpoints are under `/api/`. Authenticated endpoints need the header:

```
Authorization: Bearer <access_token>
```

### Auth & account

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/signup/` | — | Register (multipart: `first_name`, `email`, `phone_number`, `password`, `profile_image`, `student_id_image`). Account starts unapproved. |
| POST | `/api/token/` | — | Log in with `email` + `password`. Returns `access` and `refresh`. Returns 403 if not yet approved. |
| POST | `/api/token/refresh/` | — | Exchange a `refresh` token for a new `access` token. |
| POST | `/api/forgot-password/` | — | Reset password with `email` + `new_password` (min 6 chars). |
| GET / PATCH | `/api/auth/me/` | ✅ | Get current user's profile, or PATCH a new `profile_image`. |
| POST | `/api/give-trust-badge/` | ✅ | Give a trust badge to a seller (`rated_user`: seller id). |

### Wallet

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/wallet/` | ✅ | Current balance. |
| POST | `/api/wallet/add/` | ✅ | Top up (`amount` > 0). Recorded as a wallet transaction. |
| POST | `/api/wallet/deduct/` | ✅ | Deduct `amount`; fails if balance is insufficient. |

### Products

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/products/` | ✅ | List active, unsold products (excludes your own). |
| POST | `/api/products/` | ✅ | Create a listing (multipart for `primary_image`). |
| GET | `/api/products/{id}/` | ✅ | Product details. |
| PUT / PATCH / DELETE | `/api/products/{id}/` | ✅ owner | Update or delete your own listing. |
| GET | `/api/products/my/` | ✅ | Your active listings. |
| PATCH | `/api/products/{id}/custom-update/` | ✅ owner | Update a listing and send it back for admin approval. |
| POST | `/api/products/record-sale/` | ✅ | Buy a product (`product_id`, `amount`). Marks it sold. |

**Query parameters for `GET /api/products/`:**

- Filter: `?category=books`, `?condition=used_good`
- Search title/description: `?search=calculator`
- Sort: `?ordering=price`, `?ordering=-created_at`

Condition values: `new`, `used_like_new`, `used_good`, `used_fair`.

### Favourites

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/favorites/` | ✅ | Your favourites. |
| POST | `/api/favorites/` | ✅ | Add a product to favourites. |
| DELETE | `/api/favorites/{id}/` | ✅ | Remove a favourite. |

### Other

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check — confirms the API is running. |
| — | `/admin/` | Django admin panel. |

## Admin workflow

Log in at `/admin/` with a superuser account.

- **Signup Requests** — lists students awaiting approval, with a link to their student ID image. Select and run *Approve selected signup requests*.
- **Pending products** — new or edited listings awaiting approval. Use *Approve* to publish or *Reject* to delete.
- **Products**, **Students**, **Wallet transactions** and **Product sale transactions** are available for general management.

## Deployment (AWS Elastic Beanstalk)

The app is set up for Elastic Beanstalk's Python platform:

- [.ebextensions/01_django.config](.ebextensions/01_django.config) sets the WSGI path (`swapex.wsgi:application`) and runs `collectstatic` on deploy.
- Set the environment variables above in the EB environment configuration (database, S3, `DJANGO_SECRET_KEY`).
- With `DB_NAME` set, HTTPS redirect, secure cookies and HSTS are turned on automatically.
- Allowed hosts include `swapex.art`, `www.swapex.art` and `*.elasticbeanstalk.com`.

Run migrations against the production database after deploying model changes:

```bash
eb ssh
source /var/app/venv/*/bin/activate && cd /var/app/current
python manage.py migrate
```

## CORS

Allowed origins are set in [swapex/settings.py](swapex/settings.py): `swapex.art`, `www.swapex.art`, local dev ports `5173`/`3000`, and Vercel preview deployments matching `swapex-verceldeployment*.vercel.app`.
