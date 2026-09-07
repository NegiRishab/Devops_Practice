## Repository Types in Nexus

### 1. Proxy Repository

A Proxy Repository acts as a link to a remote/public repository.

Examples:

- Maven Central
- npm Registry
- PyPI
- Docker Hub

### How it works

1. Developer requests a dependency.
2. Nexus checks whether it exists in the local cache.
3. If found, Nexus serves it directly.
4. If not found, Nexus downloads it from the remote repository.
5. Nexus stores a copy locally for future requests.

### Benefits

- Faster builds
- Reduced internet usage
- Dependency caching
- Better security and control

---

### 2. Hosted Repository

A Hosted Repository is the primary storage location inside Nexus.

Used for storing:

- Company build artifacts
- Internal libraries
- Private Docker images
- Release packages

### Example

```
Developer → Build Application → Upload Artifact → Hosted Repository
```

Artifacts stored here are managed entirely by the organization.

---

### 3. Group Repository

A Group Repository combines multiple repositories into a single endpoint.

Without Group Repository:

```
Repo URL 1
Repo URL 2
Repo URL 3
Repo URL 4
```

Applications and CI/CD pipelines would need to configure multiple URLs.

With Group Repository:

```
Group Repository
      |
  ----------------
  |      |      |
Proxy  Hosted  Other Repos
```

Only one URL is configured in:

- Maven
- Gradle
- Jenkins pipelines
- Applications

Nexus automatically searches the member repositories.

### Benefits

- Single repository endpoint
- Easier configuration
- Simplified CI/CD setup

---

# Project Workflow Example

### User and Permissions

Create users and assign roles:

- Read access
- Upload access
- Admin access

Users authenticate to Nexus and interact with repositories according to their permissions.

---

### Build and Publish

Example Java application:

1. Configure Nexus repository URL in Maven or Gradle.
2. Build the application.
3. Generate artifact (JAR/WAR).
4. Publish artifact to Nexus Hosted Repository.

Example:

```
Code → Build → JAR → Nexus Hosted Repository
```

---

# Nexus REST API

Nexus provides REST APIs that can be accessed using tools like:

```
curl
```

Common operations:

- List repositories
- Upload artifacts
- Download artifacts
- Search components
- Delete components
- Manage users and permissions

### Why use APIs?

Useful for automation in:

- Jenkins
- GitLab CI/CD
- GitHub Actions
- Shell scripts

You don't memorize API endpoints; you typically refer to documentation when building automation.

---

# Blob Stores

A Blob Store is the physical storage location where Nexus saves repository data.

Think of it as the actual disk storage behind the repositories.

### Relationship

```
Repository
     |
Blob Store
     |
Files Stored on Disk
```

### Example

```
Hosted Repository
       |
Default Blob Store
       |
Artifacts Stored
```

A repository does not directly store files.

The repository uses a Blob Store, and the Blob Store stores the actual data.

### Benefits

- Centralized storage
- Better storage management
- Easier backup and maintenance

---

# Components vs Assets

This is a common interview question.

### Component

A Component is the logical package stored in Nexus.

Examples:

- myapp-1.0.jar
- nginx:1.25 Docker image
- spring-core dependency

Think of a component as the complete software package.

---

### Asset

Assets are the actual files that belong to a component.

### Example (Maven)

Component:

```
myapp-1.0
```

Assets:

```
myapp-1.0.jar
myapp-1.0.pom
myapp-1.0.sha1
```

One component can contain multiple assets.

---

### Docker Example

Component:

```
nginx:1.25
```

Assets:

```
Layer 1
Layer 2
Layer 3
Manifest File
```

Docker image layers are stored as assets.

---

# Cleanup Policies

Cleanup Policies automatically remove old or unused artifacts.

### Common Use Cases

- Delete old snapshot versions
- Remove unused packages
- Free storage space
- Keep repositories clean

### Example

```
Keep last 10 versions
Delete versions older than 90 days
```

### Benefits

- Saves storage
- Improves repository maintenance
- Reduces repository size