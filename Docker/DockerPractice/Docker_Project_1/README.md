# Todo app (Express + MongoDB)

A small todo API with a single-page UI (`index.html`). Data is stored in MongoDB. The project is set up so you can run it locally or with Docker Compose for practice.

## What you need

- **Node.js** (v18 or newer recommended) for running on your machine
- **MongoDB** reachable from the app (local install or a container)
- **Docker** and **Docker Compose** if you want the full stack in containers

---

## Run on your machine (no Docker)

### 1. Install dependencies

```bash
npm install
```

### 2. Start MongoDB

MongoDB must be listening where the app expects it. By default `server.js` uses:

`mongodb://admin:pass@mongo:27017/todosdb?authSource=admin`

That hostname (`mongo`) is for Docker networks. **On your laptop**, either:

- Point Mongo at **`localhost`** and create a user that matches, or  
- Override the URI with an environment variable (see below).

Example if Mongo has no auth on localhost:

```bash
export MONGO_URI="mongodb://127.0.0.1:27017/todosdb"
npm start
```

Example if you use the same admin user as in Compose (`admin` / `pass`):

```bash
export MONGO_URI="mongodb://admin:pass@127.0.0.1:27017/todosdb?authSource=admin"
npm start
```

### 3. Open the app

- **App:** [http://localhost:3000](http://localhost:3000)

The server waits and **retries** if MongoDB is not ready yet (useful when Mongo starts slowly).

---

## Run with Docker Compose

Compose file: **`mongo.yml`**. It runs three services:

| Service        | Role                         | Host port |
|----------------|------------------------------|-----------|
| **my-app**     | This Node todo app           | **3000**  |
| **mongo**      | MongoDB with persisted data  | **27017** |
| **mongo-express** | Web UI to browse MongoDB | **8081**  |

### 1. Build the app image

Compose expects image **`myapp:2.0`** (see `mongo.yml`). Build it from the project root:

```bash
docker build -t myapp:2.0 .
```

### 2. Start everything

```bash
docker compose -f mongo.yml up -d
```

To watch logs:

```bash
docker compose -f mongo.yml logs -f
```

### 3. Open in the browser

| What              | URL |
|-------------------|-----|
| Todo app          | [http://localhost:3000](http://localhost:3000) |
| Mongo Express     | [http://localhost:8081](http://localhost:8081) |

**Mongo Express login** (HTTP Basic Auth):

- Username: `admin`  
- Password: `pass`

That is only for the Mongo Express web UI. The MongoDB server itself uses the same **`admin` / `pass`** pair as root (see `mongo.yml`).

### 4. Stop

```bash
docker compose -f mongo.yml down
```

Mongo data is kept in the **`mongo-data`** volume until you remove it.

---

## Environment variables

| Variable | Purpose | Default in code |
|----------|---------|------------------|
| `MONGO_URI` | Full MongoDB connection string | See `server.js` (Docker-friendly default uses host `mongo`) |
| `PORT` | HTTP port | `3000` |
| `MONGO_RETRY_INITIAL_MS` | First retry delay if DB is down | `1000` |
| `MONGO_RETRY_MAX_MS` | Max delay between retries | `15000` |

You can put these in a **`.env`** file in the project root (`dotenv` loads it).

---

## Project layout

| File | Role |
|------|------|
| `server.js` | Express API, static `index.html`, Mongoose models |
| `index.html` | Todo UI (calls `/api/todos`) |
| `mongo.yml` | Docker Compose: app + MongoDB + Mongo Express |
| `Dockerfile` | Builds the Node app image tagged as `myapp:2.0` for Compose |

---

## API (quick reference)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/todos` | List todos |
| `POST` | `/api/todos` | Body: `{ "title": "..." }` |
| `PATCH` | `/api/todos/:id` | Body: `{ "title": "..." }` and/or `{ "completed": true }` |
| `DELETE` | `/api/todos/:id` | Delete one |

---

## Troubleshooting

- **Compose: “pull access denied” or image not found for `my-app`** — Build first: `docker build -t myapp:2.0 .`
- **App container keeps logging “MongoDB not ready”** — Ensure the **mongo** service is running and on the same Compose network; the default URI uses hostname **`mongo`**.
- **Port already in use** — Change the host mapping in `mongo.yml` (e.g. `3001:3000`) or stop the other process using that port.
