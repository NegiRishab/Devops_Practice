# Concept 2 → Docker Socket Mount

```
-v /var/run/docker.sock:/var/run/docker.sock
```

Concept:

## Bind Mount + Docker Socket Sharing

Purpose:

- allow Jenkins container to control HOST Docker daemon

This enables:

```
docker build
docker run
dockerps
```

inside Jenkins container.

---

# Architecture

```
+----------------------------------+
| HOST MACHINE                     |
|                                  |
| Docker Daemon                    |
|    ↑                             |
| /var/run/docker.sock             |
|                                  |
| Jenkins Container                |
|   docker CLI                     |
|        ↑                         |
| mounted docker.sock              |
+----------------------------------+
```

---

# Important Concept Name

This setup is called:

# Docker Outside of Docker (DooD)

Because:

- Docker daemon runs on HOST
- Container only uses the socket

NOT:

- Docker-in-Docker (DinD)

---

# Docker CLI  --->  docker.sock  ---> Docker Daemon  

so when i attached docker.sock host to container i am directly setting the container comunication with docker engine that is running on host