# Foodie Deployment Guide

## Backend Deployment to Render

### Step 1: Push Code to GitHub
1. Create a GitHub repository
2. Push your foodie project to GitHub
3. Make sure to include:
   - backend/ folder with all files
   - render.yaml file
   - requirements.txt
   - .env file (or set environment variables in Render)

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up (free)
3. Click "New" → "Web Service"

### Step 3: Connect GitHub
1. Click "Connect GitHub"
2. Authorize Render to access your GitHub
3. Select your foodie repository
4. Click "Connect"

### Step 4: Configure Render Service
Render will auto-detect Python from render.yaml:
- **Name:** foodie-backend
- **Region:** Choose nearest region
- **Branch:** main
- **Root Directory:** backend
- **Build Command:** pip install -r requirements.txt
- **Start Command:** python main.py

### Step 5: Set Environment Variables
In Render dashboard → Environment:
```
DATABASE_URL=sqlite:///./foodie.db
SECRET_KEY=your_secret_key_here
```

### Step 6: Deploy
Click "Create Web Service"
Wait for deployment to complete (2-3 minutes)

### Step 7: Get Backend URL
After deployment, Render will provide a URL like:
https://foodie-backend.onrender.com

## Frontend Deployment to Netlify

### Step 1: Update API URL
Edit `frontend/js/api.js`:
```javascript
const API_BASE_URL = 'https://foodie-backend.onrender.com';
```

### Step 2: Deploy to Netlify
1. Go to https://netlify.com
2. Drag and drop the `frontend` folder
3. Or connect to GitHub

### Step 3: Done!
Your site will be live at: https://your-site.netlify.app

## Alternative: Railway Deployment

### Step 1: Go to railway.app
### Step 2: New Project → Deploy from GitHub
### Step 3: Select your repository
### Step 4: Railway auto-detects Python
### Step 5: Set environment variables
### Step 6: Deploy

## Important Notes

### Database on Render
- SQLite works but data is lost on redeploy
- For production, use PostgreSQL
- Add PostgreSQL database in Render dashboard
- Update DATABASE_URL in environment variables

### CORS Configuration
Make sure your backend allows your Netlify domain:
Update `backend/config/settings.py`:
```python
CORS_ORIGINS = ["https://your-site.netlify.app", "http://localhost:5500"]
```

### Free Tier Limitations
- Render: Free tier spins down after 15 min inactivity
- First request takes ~30 seconds to wake up
- Railway: Similar limitations
- Netlify: Always active

## Troubleshooting

### Backend Not Starting
- Check Render logs
- Verify requirements.txt is correct
- Check environment variables

### Frontend API Errors
- Verify API_BASE_URL is correct
- Check CORS configuration
- Check backend is running

### Database Issues
- Use PostgreSQL for production
- Set up persistent database
