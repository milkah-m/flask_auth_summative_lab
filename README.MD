# Mood Tracker API (Flask + JWT)

A RESTful API built with Flask that allows users to register, log in, and track their moods over time. The system uses JWT authentication to secure routes and supports full CRUD operations on mood entries.

---

## Features

* User registration and login
* JWT-based authentication
* Secure password hashing
* Protected routes
* Create, read, update, delete moods
* Pagination for mood entries
* Seeder script using Faker for test data
* One-to-many relationship (User → Moods)

---

## Tech Stack

* Python
* Flask
* Flask SQLAlchemy
* Flask-Migrate
* PyJWT
* Werkzeug Security
* Faker (for seeding)
* SQLite (default database)

---

## Project Structure

```
app/
├── auth/              # Authentication routes (login, signup, me)
├── moods/             # Mood CRUD routes
├── models.py          # User & Mood models
├── utils.py           # JWT decorator
├── __init__.py       # App factory

seed.py                # Database seeding script
config.py              # App configuration
run.py                 # App entry point
```

---

## Setup Instructions

### 1. Clone repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up database

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 5. Seed database (IMPORTANT)

```bash
python seed.py
```

This creates:

* 50 users
* 250 mood entries

### 6. Run server

```bash
flask run
```

---

## Authentication Flow

### 1. Register user

```
POST /signup
```

### 2. Login

```
POST /login
```

Returns:

```json
{
  "token": "your.jwt.token"
}
```

### 3. Use token in requests

Add header:

```
Authorization: Bearer <token>
```

---

## API Endpoints

### Auth

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| POST   | /signup  | Register new user |
| POST   | /login   | Login user        |
| GET    | /me      | Get current user  |

---

### Moods (Protected)

| Method | Endpoint    | Description               |
| ------ | ----------- | ------------------------- |
| GET    | /moods      | Get all moods (paginated) |
| POST   | /moods      | Create mood               |
| PUT    | /moods/<id> | Update mood               |
| DELETE | /moods/<id> | Delete mood               |

---

## Pagination

Moods are paginated:

```
GET /moods?page=1
```

Default:

* 5 items per page

If page does not exist it returns an empty list.

---

## Seed Data

The seed file generates:

* 50 users
* 5 moods per user
* Mood notes that use pre-set templates

To reset database:

```bash
python seed.py
```

---

## Security

* Passwords hashed before storage
* JWT used for stateless authentication
* Protected routes require valid token
* Unauthorized access returns 401 errors

---

## Testing Workflow

1. Run seed.py
2. Start server
3. Login via /login
4. Copy token
5. Test /me
6. Test /moods
7. Test pagination
8. Test CRUD operations
9. Test unauthorized access

---

## Status Codes

* 200 Success
* 201 Created
* 400 Bad request
* 401 Unauthorized
* 404 Not found

---

## Author: Milkah Mwangi

Built as a Flask backend project focusing on authentication, REST APIs, and database relationships.
