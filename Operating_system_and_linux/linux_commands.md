# Linux Basics – Users, Groups, Permissions & Commands

## 1. Linux Accounts

In **Linux**, multiple users can access the same system. Each user has a separate account.

### 1. Superuser Account (Root)

- The **root user** is the **superuser** in Linux.
- It has **unrestricted permissions**.
- Root can:
    - Modify any file
    - Install software
    - Manage users
    - Change system settings

⚠️ **Best Practice:**

Avoid running normal tasks as root for security reasons.

---

### 2. Regular User Account

- A **regular user** is created for login and normal work.
- Each user has a **home directory**.

Example:

```
/home/username
```

Example user home:

```
/home/narshing
```

This directory stores:

- personal files
- configuration files
- scripts

---

### 3. Service Users

Service users are mainly used in **Linux server distributions**.

Example services:

- Web server
- Database
- Monitoring tools

**Best practice:**

Each service should run with **its own user account** instead of the root user.

Benefits:

- Better security
- Limits damage if a service is compromised

---

# 2. Multiple Users on a Server

In organizations, many team members use the same server.

### Why each team member needs their own user

1. **Security**
    - Users should have **non-root accounts**.
2. **Permission Control**
    - Permissions can be assigned to each user.
3. **Traceability**
    - Easy to track **who did what on the system**.

---

# 3. Groups in Linux

Linux supports **group-based access control**.

### Two Types of Permission Assignment

### 1. User-Level Permissions

Permissions are assigned **directly to a user**.

### 2. Group-Level Permissions

Users are added to **Linux groups**, and permissions are given to the group.

Example:

```
devops group
backend group
admins group
```

### Benefits of Groups

- Easy user management
- Add a user to a group → user automatically gets group permissions
- Remove user → permissions removed automatically

This is a **very important concept in Linux user management**.

---

# 4. User Information in Linux

User details are stored in:

```
/etc/passwd
```

You can view it using:

```
vim /etc/passwd
```

This file contains details of all users.

### Structure of `/etc/passwd`

```
username:password:userid:groupid:userdetails:homedirectory:shell
```

Example:

```
narshing:x:1001:1001:Narshing:/home/narshing:/bin/bash
```

Fields explained:

| Field | Meaning |
| --- | --- |
| username | User login name |
| password | Password placeholder |
| userid (UID) | Unique user ID |
| groupid (GID) | Primary group ID |
| user details | Description |
| home directory | User home folder |
| shell | Default shell |

---

# 5. File Ownership

Files in Linux belong to:

- **User (owner)**
- **Group**

### Change File Ownership

Change both user and group:

```
sudo chown username:groupname filename
```

Change only group:

```
sudo chgrp groupname filename
```

Change only owner:

```
sudo chown username filename
```

---

# 6. Linux File Permissions

Example:

```
-rw-rw-r-- 1 narshing devops 401 Feb 28 08:04 new.js
```

### File Type

First character shows file type:

| Symbol | Meaning |
| --- | --- |
| `-` | File |
| `d` | Directory |

---

### Permission Structure

```
rwx rwx rwx
│   │   │
│   │   └── Other users
│   └────── Group
└────────── Owner (User)
```

---

### Permission Meaning

| Symbol | Meaning |
| --- | --- |
| r | Read |
| w | Write |
| x | Execute |
| - | No permission |

---

# 7. Changing Permissions

Command:

```
chmod
```

### Give group full permission

```
sudo chmod g+rwx filename
```

### Remove group permission

```
sudo chmod g-rwx filename
```

### Permission Symbols

| Symbol | Meaning |
| --- | --- |
| u | User (owner) |
| g | Group |
| o | Others |

Example:

```
chmod u+x script.sh
```

---

# 8. Pipe (`|`) in Linux

A **pipe** sends the output of one command to another command.

Example:

```
history | grep sudo
```

Explanation:

- `history` → shows command history
- `grep` → filters text

---

### Using Pipe with `less`

```
history | grep sudo | less
```

- `less` allows scrolling through long output.

---

# 9. Useful Command: `grep`

`grep` is used to **search text in command output or files**.

Example:

```
ps aux | grep nginx
```

---

# 10. Running Multiple Commands

You can run commands sequentially using `;`

Example:

```php
clear ; sleep 1 ; echo "I love coding"
```

Steps:

1. Clears terminal
2. Waits 1 second
3. Prints message