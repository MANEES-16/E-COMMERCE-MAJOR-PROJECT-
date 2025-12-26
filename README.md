# Major Project E-commerce App

This repository contains a Django REST backend and a React/Redux frontend for a simple e-commerce store. Follow the steps below to install dependencies, set up the database, and run both servers locally.

## 1. Prerequisites
- Python 3.13 (other 3.11+ versions should work)
- Node.js 18+
- npm 9+
- Git (optional but recommended)

## 2. Backend Setup (Django)
1. Open a terminal in the backend folder:
   ```powershell
   cd backend
   ```
2. Create and activate a virtual environment (Windows PowerShell example):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Apply database migrations and seed initial data:
   ```powershell
   python manage.py migrate
   python manage.py loaddata base/fixtures/initial_data.json  # optional if you create fixtures
   ```
   > Note: This project already includes a migration that seeds sample products and an admin user when you run `python manage.py migrate`.
5. Start the development server:
   ```powershell
   python manage.py runserver
   ```
   The API becomes available at http://127.0.0.1:8000/.

### Admin Access
- URL: http://127.0.0.1:8000/admin/
- Email: admin@example.com
- Password: admin123

## 3. Frontend Setup (React)
1. Open a second terminal in the frontend folder:
   ```powershell
   cd frontend
   ```
2. Install JavaScript dependencies:
   ```powershell
   npm install
   ```
3. Start the React development server:
   ```powershell
   npm start
   ```
   The app opens at http://localhost:3000 and proxies API calls to the Django backend.

## 4. Project Structure
```
backend/   # Django project (REST API, models, migrations)
frontend/  # React + Redux UI
```

## 5. Running Tests
- Backend tests:
  ```powershell
  cd backend
  python manage.py test
  ```
- Frontend tests:
  ```powershell
  cd frontend
  npm test
  ```

## 6. Helpful Tips
- Always keep both servers running (`python manage.py runserver` and `npm start`) for full functionality.
- Product images live under frontend/public/images. Ensure filenames in the database match actual assets.
- Use `.env` files if you need to override defaults (e.g., API base URLs, secret keys).
- Version control: the repository includes a `.gitignore` that excludes virtual environments, build artifacts, database files, and other local-only assets for both Python and Node workflows.

## 7. Production Build (Optional)
- Frontend: `npm run build` outputs optimized assets under frontend/build.
- Backend: configure environment variables and use a production-ready WSGI/ASGI server (e.g., Gunicorn) before deployment.
