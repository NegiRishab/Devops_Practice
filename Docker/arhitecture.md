# 

Docker works using **3 main components**:

## 1. CLI (Command Line Interface)

- Used by the user to run commands
- Example:
    
    ```
    docker run
    docker build
    ```
    

👉 CLI sends requests to Docker API

---

## 2. Docker API

- Acts as a **bridge**
- Receives requests from CLI
- Sends them to Docker Server (Daemon)

---

## 3. Docker Server (Docker Daemon)

- Main engine of Docker
- Responsible for:
    - Running containers
    - Managing images
    - Handling networking & storage

---

# ⚙️ Inside Docker Server (Daemon)

Docker server has **4 main responsibilities**:

---

## 1. Container Runtime

- Runs and manages containers
- Handles container lifecycle:
    - Start
    - Stop
    - Restart

---

## 2. Image Management

- Pull images from registry (Docker Hub)
- Store images locally
- Remove unused images

---

## 3. Volumes (Storage)

- Used for **data persistence**
- Data stays even if container is deleted

---

## 4. Networking

- Allows containers to communicate
- Provides:
    - IP address
    - DNS (service name communication)

---

## 5. Build System (Extra)

- Builds custom Docker images using `Dockerfile`

---

# 🔄 Flow (Simple)

```
CLI → API → Docker Daemon → Containers
```

---

# 💡 One-line summary

👉 Docker CLI sends commands to the daemon via API, and the daemon manages containers, images, storage, and networking.