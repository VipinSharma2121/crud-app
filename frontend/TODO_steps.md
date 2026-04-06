# OTP-Protected User Creation Steps

## Plan Progress Tracker

### 1. [DONE] Create this TODO_steps.md - Setup tracking
### 2. [DONE] Edit frontend/app/views.py - Remove direct save, just render form
### 3. [DONE] Edit frontend/templates/create_user.html - Add AJAX send-otp + OTP modal JS + create-user
### 4. [DONE] Edit backend/routes/user.py - Change username→first_name, hash password before save (polished upsert, uuid image, upload fix)
### 5. [DONE] Minor frontend JS/backend polishes
### 6. [TODO] Test integration
   - Backend: cd backend && uvicorn main:app --reload --port 8000
   - Frontend: cd frontend && python manage.py runserver
   - Create user → check console OTP → verify → check backend/db.sqlite3
### 7. [TODO] Update dashboard to fetch from FastAPI /users/ (optional future)

**Current Status:** Starting implementation...

**Notes:** 
- FastAPI: http://localhost:8000
- OTP printed to FastAPI console for testing (replace with email later)
- Backend uses SQLite backend/db.sqlite3 (separate from Django)

