# 🚀 Community Feed

A full-stack community feed application built with Django REST Framework and React.
Users can create posts, like posts and comments, earn karma, and view a real-time leaderboard.

## 🚀 Live Demo:
### Frontend: https://connect4-hazel-ten.vercel.app/
### Backend: https://connect4-production-d2c5.up.railway.app

## 🧠 Features

1. Create and view posts

2. Like posts and comments

3. Nested comments (replies)

4. Karma system (likes & comments add karma)

5. Top users leaderboard (last 24 hours)

6. Fully deployed backend + frontend

## 🛠 Tech Stack
### Backend

Django

Django REST Framework

PostgreSQL

Gunicorn

Frontend

React (Vite)

Tailwind CSS

Deployment

Backend: Railway

Frontend: Vercel

Database: Railway PostgreSQL

🌍 Live URLs

Frontend: https://<your-vercel-url>

Backend API: https://community-feed-production-5182.up.railway.app

📂 Project Structure
Community-Feed/
│
├── backend/
│ ├── backend/
│ ├── apps/
│ ├── manage.py
│ └── requirements.txt
│
└── frontend/
├── src/
├── package.json
└── vite.config.js

⚙️ Running Locally
1️⃣ Clone the repository
git clone https://github.com/<your-username>/community-feed.git
cd Community-Feed

2️⃣ Backend Setup (Django)
Create virtual environment
cd backend
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Environment Variables

Create a .env file inside backend/:

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/community_feed

You can also use SQLite locally by removing DATABASE_URL.

Run migrations
python manage.py migrate

Create superuser (optional)
python manage.py createsuperuser

Start backend server
python manage.py runserver

Backend runs at:

http://127.0.0.1:8000/

3️⃣ Frontend Setup (React)
cd ../frontend
npm install

Frontend Environment Variables

Create .env in frontend/:

VITE_API_BASE_URL=http://127.0.0.1:8000/api

Start frontend
npm run dev

Frontend runs at:

http://localhost:5173/

🔁 How Local Flow Works

React → calls Django REST API

Django → reads/writes to PostgreSQL

Likes & comments → increase user karma

Leaderboard updates dynamically

🚀 Deployment Notes
Backend (Railway)

Uses gunicorn backend.wsgi

Port is auto-detected by Railway

PostgreSQL provisioned via Railway plugin

Migrations run manually against Railway DB

Frontend (Vercel)

Built with Vite

Uses VITE_API_BASE_URL env variable

Automatically redeployed on push

🧪 API Endpoints (Sample)
GET /api/feed/
POST /api/feed/<post_id>/like/
POST /api/feed/<post_id>/comment/
GET /api/feed/leaderboard/

⚠️ Important Notes

Authentication is not implemented (user_id is simulated)

Designed for learning & demonstration

Production auth can be added later

📌 Future Improvements

JWT authentication

User profiles

Edit/delete posts & comments

WebSocket real-time updates

👤 Author

Anurag
Computer Science Student @ GGSIPU
Aspiring Full-Stack Developer
