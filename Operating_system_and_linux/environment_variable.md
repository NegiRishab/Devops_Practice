# Environment Variables in Linux

Environment variables are **key–value pairs** used by the system and applications to configure how programs run.

Example structure:

```
KEY=value
```

Example:

```
USER=vicky
HOME=/home/vicky
```

These variables store **information about the user's environment** and system configuration.

Environment variables are heavily used in **Linux systems and shell environments like Bash.

---

# 1. User Environment

Each user in Linux has **their own environment**.

That means every user can configure their own preferences.

Examples of user-specific settings:

- Default shell
- Text editor
- Browser
- Terminal settings
- Language settings
- Paths for executables

Example:

User **vicky** may use:

```
editor=vim
shell=bash
```

Another user could choose:

```
editor=nano
shell=zsh
```

So the OS needs a way to **store and read these preferences**, which is done through **environment variables**.

---

# 2. Viewing Environment Variables

To see all environment variables:

```
printenv | less
```

Explanation:

- `printenv` → displays all environment variables
- `less` → scroll through long output

---

### Filter specific variables

Example:

```
printenv |grep USER
```

Output example:

```
USERNAME=vicky
USER=vicky
```

---

### Access variable value

Use `$` before the variable name.

Example:

```
echo$USER
```

Output:

```
vicky
```

---

# 3. Creating Environment Variables

We use the `export` command.

Example:

```
exportDB_USERNAME=dbuser
exportDB_PASSWORD=secretpower
```

Now check them:

```
printenv |grep DB
```

Example output:

```
DB_PASSWORD=secretpower
DB_USERNAME=dbuser
```

---

# 4. Removing Environment Variables

Use the `unset` command.

Example:

```
unset DB_USERNAME
```

Check again:

```
printenv |grep DB
```

Now only remaining variable appears.

---

# 5. Temporary vs Permanent Variables

### Temporary Variables

Variables created with `export` only exist in the **current terminal session**.

Example:

```
exportMY_VAR=test
```

If you:

- close the terminal
- open a new terminal

The variable **disappears**.

---

### Permanent Environment Variables

To make variables **permanent**, they must be stored in configuration files.

Common files:

| File | Scope |
| --- | --- |
| `/etc/environment` | system-wide variables |
| `~/.bashrc` | user-specific shell settings |
| `~/.profile` | login shell configuration |

---

# 6. Example: Setting a Permanent Variable

Open `.bashrc`

```
vim ~/.bashrc
```

Add:

```
exportDB_USERNAME=dbuser
```

Apply changes:

```
source ~/.bashrc
```

Now the variable will exist **every time you open the terminal**.

---

# 7. The PATH Environment Variable

One of the most important variables is **PATH**.

It stores directories where executable programs are located.

Example:

```
echo$PATH
```

Output example:

```
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

The system searches these directories when you run a command.

Example:

```
ls
```

The shell looks for `ls` in each directory listed in PATH.

---

# 8. Adding a Directory to PATH

You can add your own directory to PATH.

Example:

```
exportPATH=$PATH:/home/vicky
```

Meaning:

- Keep the existing PATH
- Add `/home/vicky` to it

---

# 9. Creating Custom Commands Using PATH

Example:

Create a script:

```
vim ~/welcome
```

Add:

```
#!/bin/bash
echo"Welcome to my system!"
```

Make it executable:

```
chmod+x ~/welcome
```

Now add home directory to PATH:

```
exportPATH=$PATH:/home/vicky
```

Now you can run:

```
welcome
```

from **any directory**.

---

# 10. User-Level vs System-Level Environment Variables

### User-Level

Stored in:

```
~/.bashrc
```

These variables apply **only to that user**.

Example:

User `vicky` creates:

```
export EDITOR=vim
```

Only **vicky** will see it.

---

### System-Level (Global)

Stored in:

```
/etc/environment
```

These variables apply **to all users on the system**.

Example:

```
JAVA_HOME=/usr/lib/jvm/java
```

Now every user will have access.

---

# 11. Why Environment Variables Are Important (DevOps)

Environment variables are widely used in DevOps tools like:

- Docker
- Kubernetes
- Jenkins
- Node.js

Example in applications:

```
DB_HOST
DB_USERNAME
DB_PASSWORD
API_KEY
PORT
```

Instead of hardcoding secrets in code, they are stored as **environment variables**.

This improves **security and flexibility**.

---

# Key Summary

Environment variables:

- store system configuration
- store user preferences
- allow applications to read settings

Important commands:

| Command | Purpose |
| --- | --- |
| `printenv` | show environment variables |
| `echo $VAR` | print specific variable |
| `export` | create variable |
| `unset` | remove variable |
| `source` | reload config file |