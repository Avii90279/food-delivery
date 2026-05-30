# Foodie Project Setup Guide

## Prerequisites
- Python 3.8 or higher
- Node.js (not required - using vanilla JavaScript)
- Web browser

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file in backend directory:
```
DATABASE_URL=sqlite:///./foodie.db
SECRET_KEY=your_secret_key_here
```

### 3. Seed Database
```bash
python seed_data.py
```

### 4. Run Backend Server
```bash
python main.py
```
Backend will run on: http://localhost:8000

## Frontend Setup

### 1. No Dependencies Required
Frontend uses vanilla HTML, CSS, JavaScript - no npm install needed.

### 2. Run Frontend Server
```bash
cd frontend
python -m http.server 5500
```
Frontend will run on: http://localhost:5500

## Quick Start (Windows)

### Using Batch Files

**Start Backend:**
```bash
cd backend
python main.py
```

**Start Frontend:**
```bash
cd frontend
python -m http.server 5500
```

## Required Python Libraries

Backend requires these libraries (see `backend/requirements.txt`):
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-multipart==0.0.6
- pydantic[email]==2.5.0
- python-dotenv==1.0.0

## Database Configuration

### SQLite (Default)
No additional setup needed. Database file: `backend/foodie.db`

### PostgreSQL (Optional)
Update `.env` file with PostgreSQL connection string:
```
DATABASE_URL=postgresql://username:password@host:5432/database
```

## Access URLs

- **Frontend:** http://localhost:5500
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Default Admin Credentials

- Email: admin@foodie.com
- Password: admin123

## Troubleshooting

### Backend not starting
- Check if port 8000 is already in use
- Verify Python dependencies are installed
- Check `.env` file configuration

### Frontend not starting
- Check if port 5500 is already in use
- Verify you're in the `frontend` directory

### Orders not showing
- Make sure you're logged in
- Check browser console for errors
- Verify backend is running
