# 🚀 Community Feed

A full-stack community feed application built with Django REST Framework and React.
Users can create posts, like posts and comments, earn karma, and view a real-time leaderboard.

## 🚀 Live Demo:

### Frontend: https://community-feed-zeta.vercel.app/

### Backend: https://community-feed-production-5182.up.railway.app/

## 🧠 Features

1. Create and view posts

2. Like posts and comments

3. Nested comments (replies)

4. Karma system (likes & comments add karma)

5. Top users leaderboard (last 24 hours)

6. Fully deployed backend + frontend

## 🛠 Tech Stack

### Backend

• Django

• Django REST Framework

• PostgreSQL

• unicorn

### Frontend

• React (Vite)

• Tailwind CSS

## Deployment

1. Backend: Railway

2. Frontend: Vercel

3. Database: Railway PostgreSQL

📂 Project Structure

```
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
```

## ⚙️ Running Locally

### 1️⃣ Clone the repository

```
git clone https://github.com/Anurag10303/Community-Feed
cd Community-Feed
```

### 2️⃣ Backend Setup (Django)

```
Create virtual environment
cd backend
python -m venv venv
```

#### Activate it:

```
Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
```

#### Install dependencies

```
pip install -r requirements.txt
```

### Environment Variables

#### Create a .env file inside backend/:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/community_feed
```

#### You can also use SQLite locally by removing DATABASE_URL.

##### Run migrations

```
python manage.py migrate
```

##### Create superuser (optional)

```
python manage.py createsuperuser
```

##### Start backend server

```
python manage.py runserver
```

### Backend runs at:

```
http://127.0.0.1:8000/
```

### 3️⃣ Frontend Setup (React)

```
cd ../frontend
npm install
```

#### Frontend Environment Variables

##### Create .env in frontend/:

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### Start frontend

```
npm run dev
```

### Frontend runs at:

```
http://localhost:5173/
```

## 🔁 How Local Flow Works

• React → calls Django REST API

• Django → reads/writes to PostgreSQL

• Likes & comments → increase user karma

• Leaderboard updates dynamically

## 🚀 Deployment Notes

### Backend (Railway)

1. Uses gunicorn backend.wsgi

2. Port is auto-detected by Railway

3. PostgreSQL provisioned via Railway plugin

4. Migrations run manually against Railway DB

### Frontend (Vercel)

1. Built with Vite

2. Uses VITE_API_BASE_URL env variable

3. Automatically redeployed on push

## 🧪 API Endpoints (Sample)

```
GET /api/feed/
POST /api/feed/<post_id>/like/
POST /api/feed/<post_id>/comment/
GET /api/feed/leaderboard/
```

## ⚠️ Important Notes

1. Authentication is not implemented (user_id is simulated)

2. Designed for learning & demonstration

3. Production auth can be added later

## 📌 Future Improvements

1. JWT authentication

2. User profiles

3. Edit/delete posts & comments

4. WebSocket real-time updates

## 👤 Author

Anurag

Computer Science Student @ GGSIPU

Aspiring Full-Stack Developer
