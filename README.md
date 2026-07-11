# BarberEase

BarberEase is a web-based appointment and management system for small barbershops. Customers can register, log in, and book appointments; barbers can view their schedules; and the shop owner can manage services and track transactions.

## Team — RedHorse.dev

| Name | Program | Role |
|---|---|---|
| Tiara Michelle R. Bernardo | BS Information Systems | Frontend Developer |
| Justin Mangubat | BS Information Technology | Backend Developer |
| Jian Gabriel Tria | BS Information Technology | Database Designer |

## Tech Stack

- **Frontend:** Vue 3 (Vite), Vue Router, Axios
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-CORS
- **Database:** MySQL

## Features

- **Login / Register** — combined auth page with required-field validation and clear success/error feedback. Registering inserts a new record into the `user` table; logging in checks the submitted email/password against that table.
- **Services Management (CRUD)** — Create, Read, Update, and Delete barbershop services, all backed by the `services` table.
- Barber, customer, and reservation management modules.

## Project Structure

```
backend/    Flask API (models, routes, DB config)
frontend/   Vue 3 + Vite single-page app
```

## Getting Started

### 1. Database

Create a MySQL database named `barbershop_db`, then update the connection string in `backend/app.py` if your MySQL credentials differ from `root`/`root`.

```sql
CREATE DATABASE barbershop_db;
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # on Windows
# source venv/bin/activate   # on macOS/Linux

pip install flask flask-sqlalchemy flask-cors pymysql

python create_tables.py      # creates all tables, including `user`
python app.py                # runs on http://127.0.0.1:5000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev                  # runs on http://localhost:5173
```

### 4. Try it out

1. Open the frontend in your browser — you'll land on `/login`.
2. Register a new account (this writes a row to the `user` table).
3. Log in with that account (this reads the `user` table to verify credentials).
4. Use the **Services** page to add, edit, and delete services (CRUD against the `services` table).

## Notes

This is a semestral academic project. The MVP scope covers authentication, service management, barber scheduling, and appointment booking/tracking. Stretch features (notifications, online payment, analytics) are out of scope for now.
