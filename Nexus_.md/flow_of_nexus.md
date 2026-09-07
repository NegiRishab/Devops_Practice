## Artifacts

Artifacts are packaged application files generated after the build process.

Common artifact formats:

- JAR (Java Archive)
- WAR (Web Application Archive)
- ZIP
- TAR
- Docker Images
- Python Packages (.whl, .tar.gz)
- NPM Packages

Example:

- Source Code → Build → Artifact (JAR/WAR) → Store in Nexus → Deploy

---

## Artifact Repository

An Artifact Repository is a storage location where build artifacts are stored, managed, and retrieved.

Benefits:

- Centralized storage
- Version management
- Faster deployments
- Secure artifact sharing
- Avoid rebuilding the same application repeatedly

---

## Why Do We Need Nexus?

Different technologies use different package formats and repositories.

Examples:

| Technology | Artifact Type | Public Repository |
| --- | --- | --- |
| Java | JAR/WAR | Maven Central |
| JavaScript | NPM Package | npm Registry |
| Python | Wheel (.whl) | PyPI |
| .NET | NuGet Package | NuGet Gallery |

Managing all these repositories separately becomes difficult.

**Nexus Repository Manager** provides a single platform to manage all artifact types.

---

## Nexus Repository Manager

Nexus is an Artifact Repository Manager used to:

- Store build artifacts
- Retrieve artifacts
- Manage artifact versions
- Act as a central repository
- Proxy external repositories
- Improve build performance through caching

---

## Repository Types in Nexus

### 1. Hosted Repository

Repositories created and managed inside Nexus.

Used to store:

- Internal company artifacts
- Private Docker images
- Custom libraries

Example:

Developer → Upload Artifact → Nexus Hosted Repository

---

### 2. Proxy Repository

Acts as a cache for external/public repositories.

Example:

Developer requests dependency → Nexus checks cache

- If available → Serve from Nexus
- If not available → Download from Maven Central/npm/PyPI and cache it

Benefits:

- Faster builds
- Reduced internet dependency
- Better security and control

---

### 3. Group Repository

Combines multiple repositories into a single endpoint.

Example:

Maven Group

- Hosted Repository
- Proxy Repository

Developers use only one URL while Nexus searches all configured repositories.

---

# Public Repository Managers

Public repositories provide open-source packages and dependencies.

Examples:

- Maven Central
- npm Registry
- PyPI
- NuGet Gallery

Applications download libraries and frameworks from these repositories.

Nexus can connect to them using **Proxy Repositories**.

---

# Important Nexus Features

### LDAP Integration

LDAP (Lightweight Directory Access Protocol) is a protocol used to centrally manage users and authentication.

Benefits:

- Centralized user management
- Single Sign-On (SSO) support
- Role-based access control

---

### REST API

Nexus provides REST APIs for:

- Repository management
- User management
- Artifact uploads
- Automation and CI/CD integration

---

### Backup and Restore

Used for:

- Disaster recovery
- Migration
- Data protection

---

### Multi-Format Support

Supports multiple package types:

- Maven
- NPM
- Docker
- NuGet
- PyPI
- Helm
- Yum
- APT

---

### Metadata Tagging

Allows labeling artifacts with metadata such as:

- Development
- Testing
- Staging
- Production

Useful for tracking artifact promotion across environments.

---

### Cleanup Policies

Automatically removes:

- Old artifact versions
- Unused snapshots
- Obsolete packages

Benefits:

- Saves storage space
- Improves repository maintenance