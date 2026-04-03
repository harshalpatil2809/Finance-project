# Python Finance System Backend (Django + DRF)

## Overview

This project implements a finance tracking system backend with Django and Django REST Framework. It includes:
- Transaction records CRUD (income/expense)
- Role-based access (viewer, analyst, admin)
- Summary analytics (total income/expense, balance, category/ monthly breakdown, recent activity)
- JWT authentication
- Filter, search, ordering, and error handling

## Setup

1. Clone repo and cd into project directory.
2. Create and activate virtualenv:
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Apply migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## API Endpoints

- `POST /api/auth/register/` - register new user (JSON: username, email, password)
- `POST /api/auth/login/` - get JWT token (JSON: username, password)
- `POST /api/auth/token/refresh/` - refresh JWT
- `GET /api/records/` - list records (filter by transaction_type, category, date_from, date_to)
- `POST /api/records/` - create record (admin-only for write operations)
- `GET /api/records/{id}/` - retrieve record
- `PUT/PATCH /api/records/{id}/` - update record (admin-only)
- `DELETE /api/records/{id}/` - delete record (admin-only)
- `GET /api/records/summary/` - financial summaries

## Model

- `FinanceRecord`: amount, transaction_type (`income` / `expense`), category, date, description
- `UserProfile`: OneToOne with User and role field (`viewer`, `analyst`, `admin`)

## Role behavior

- `viewer`: read-only access for own records and summaries
- `analyst`: same as viewer, plus filtering/searching details
- `admin`: full CRUD for all users' records and summaries

## Validation and errors

- `amount` must be > 0
- required fields validated by serializers
- Invalid operations return HTTP 400 / 403 with JSON error details.

## Notes

- The project can be extended with pagination, unit tests, and CSV import/export.
- `admin` can set roles in Django admin.
