# Employee Management Fullstack App

This project contains:
- Java Maven backend (Spring Boot + JPA + MySQL)
- React frontend (Vite)
- Docker Compose setup
- Jenkins CI/CD pipeline files

## Features
- Employee list view
- 10 dummy employees preloaded on first run
- Add employee
- Update employee
- Delete employee
- Fields: name, email, employed status, timing, role, department

## Environment variables

Copy the template and edit values for your server:

```bash
cp .env.example .env
```

Compose reads `.env` automatically. Never commit `.env` (it may contain passwords).

For EC2 testing without a domain, set:

```bash
SERVER_HOST=13.232.43.163
VITE_API_BASE_URL=http://13.232.43.163:8080/api
```

## Run with Docker Compose

```bash
docker compose up --build -d
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080/api/employees
- MySQL: localhost:3306

## Backend local run

```bash
cd backend
mvn spring-boot:run
```

## Frontend local run

```bash
cd frontend
npm install
npm run dev
```
