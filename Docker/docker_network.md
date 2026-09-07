## 1. What is Docker networking?

**Answer:**

Docker networking allows containers to communicate:

- with each other
- with the host machine
- with external systems/internet

---

## 2. Why is Docker networking needed?

Because containers are isolated by default.

Networking helps:

- microservices communicate
- apps connect to databases
- expose applications to users

Example:

```
Frontend container → Backend container → Database container
```