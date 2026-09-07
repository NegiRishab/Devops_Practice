# Docker Basics

## 🔹 What is Docker?

👉 Docker is a **containerization (virtualization) tool** used to package applications with all their dependencies.

---

## 🔹 What is a Container?

👉 A **container** is a lightweight unit that packages:

- Application
- Dependencies
- Configuration

✔ Runs consistently across environments

---

## 🔹 Images & Registries

- **Docker Image** → Blueprint of a container
- **Container** → Running instance of an image

### 📦 Registries

- **Public Registry** → Docker Hub
    - Open and widely used
- **Private Registry**
    - Owned by a company
    - Stores internal images

---

# 🚀 How Docker Improves Development

## 🚫 Before Docker

- App depends on:
    - Node.js
    - PostgreSQL (specific version)
    - Redis (specific version)
- Every developer installs manually

### Problems:

- ❌ Version mismatch
- ❌ Setup errors
- ❌ “Works on my machine”

---

## ✅ After Docker

- Dependencies packaged in containers
- Use `docker-compose` to define services

```
docker-compose up
```

### Result:

- Same environment everywhere
- Fast setup
- No conflicts

---

# 🎯 Benefits

- Run same app with **multiple versions** (e.g., PostgreSQL 12 & 14 together)
- Isolated environments
- Fully packaged configuration
- One command setup

---

# 🚀 Deployment

## 🚫 Before Docker (Deployment)

### Process:

- Copy code to server
- Install dependencies manually
- Configure environment
- Start services

### Problems:

- ❌ Environment mismatch
- ❌ Deployment failures
- ❌ Hard scaling
- ❌ Difficult rollback

---

## ✅ After Docker (Deployment)

### Process:

- Build image
- Push to registry
- Run container

```
docker run my-app
```

### Benefits:

- ✅ Same container (dev → prod)
- ✅ No manual setup
- ✅ Fast deployment
- ✅ Easy scaling
- ✅ Easy rollback

---

# 🧱 Image & Layer Concept

👉 A **container is a running instance of an image**

👉 An **image is built using multiple layers**

- Images are **portable artifacts**

---

## 📦 Image Structure

- Most images use a **Linux base image** (lightweight)

Layers:

```
Base Image (Linux)
   ↓
Dependencies (Node, Python, etc.)
   ↓
Application Code
   ↓
Configuration
```

👉 Each step in a Dockerfile creates a **new layer**

---

# 💡 Final One-line Summary

👉 Docker packages applications with dependencies into containers, ensuring consistent development and deployment across environments.