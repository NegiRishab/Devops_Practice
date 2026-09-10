# Superhero Collection

A simple Java application with a web frontend and MySQL backend. Users add superheroes (name and power) to a collection.

## Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Frontend | HTML, CSS, JavaScript         |
| Backend  | Java 17, Spring Boot 3        |
| Database | MySQL                         |

## Prerequisites

- Java 17+
- Maven
- MySQL running locally (or wherever you point the app)

## Database setup

1. Create the database (or run `sql/schema.sql`):

   ```sql
   CREATE DATABASE superhero_db;
   ```

2. Update credentials in `src/main/resources/application.properties` if needed (default: `root` / `rootpassword`).

JPA will create/update the `superheroes` table on startup (`spring.jpa.hibernate.ddl-auto=update`).

## Run the application

```bash
mvn spring-boot:run
```

Open **http://localhost:8080**

Build a JAR:

```bash
mvn clean package
java -jar target/superhero-collection-1.0.0.jar
```

## API

| Method | Endpoint           | Body                          |
|--------|--------------------|-------------------------------|
| GET    | `/api/superheroes` | —                             |
| POST   | `/api/superheroes` | `{ "name": "...", "power": "..." }` |

## Project structure

```
├── pom.xml
├── sql/schema.sql
└── src/main/
    ├── java/com/devops/superhero/
    │   ├── SuperheroApplication.java
    │   ├── controller/SuperheroController.java
    │   ├── model/Superhero.java
    │   ├── repository/SuperheroRepository.java
    │   └── dto/SuperheroRequest.java
    └── resources/
        ├── application.properties
        └── static/          # frontend
            ├── index.html
            ├── css/style.css
            └── js/app.js
```
