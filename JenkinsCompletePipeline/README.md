# Task Board

Starter full-stack app with React frontend, Express backend, and MongoDB.

## Structure

```
backend/     Express API
frontend/    React + Vite UI
```

## Setup

**Prerequisites:** Node.js 18+, MongoDB running locally

### Backend

```bash
cd backend
cp .env.example .env
npm install
npm run dev
```

Runs on `http://localhost:5000`

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Runs on `http://localhost:5173`

## Environment

**backend/.env**

- `PORT` — API port (default: 5000)
- `MONGODB_URI` — MongoDB connection string
- `CORS_ORIGIN` — frontend URL (default: http://localhost:5173)

**frontend/.env**

- `VITE_API_URL` — API base URL (default: http://localhost:5000/api)
