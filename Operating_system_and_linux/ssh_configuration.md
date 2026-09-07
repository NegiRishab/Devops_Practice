## 1. What is SSH

- **SSH (Secure Shell)** is a **network protocol** that allows users to **securely access and manage a remote computer over the internet**.
- SSH also refers to the **set of tools/utilities** that implement this protocol.

Example use cases:

- Connect to remote servers
- Run commands remotely
- Transfer files securely

---

# 2. SSH Authentication Methods

There are **two ways to authenticate in SSH**.

## 1. Username and Password Authentication

- The **admin creates a user account** on the remote server.
- The client connects using:

```
ssh username@server-ip
```

Example:

```
ssh root@168.144.21.242
```

Then the server asks for the **password**.

### Flow

Client → enters username + password → server verifies → login allowed

### Problem

- Passwords can be **weak**
- Can be **brute-forced**
- Less secure for production systems

---

## 2. SSH Key Authentication (Recommended)

This method uses a **key pair**.

An SSH key pair contains:

- **Private Key**
- **Public Key**

### Private Key

- Stored **securely on the client machine**
- Must **never be shared**

### Public Key

- Shared with the **remote server**
- Stored in:

```
~/.ssh/authorized_keys
```

### How it works

1. Client generates key pair

```
ssh-keygen -t rsa
```

1. Two files are created:

```
~/.ssh/id_rsa        (private key)
~/.ssh/id_rsa.pub    (public key)
```

1. Copy **public key** to remote server.
2. When connecting:
- Client proves identity using **private key**
- Server verifies it with **public key**

So **no password is required**.

---

# 3. SSH Service

SSH runs as a **service on the server**.

### Important facts

- SSH server listens on **Port 22 by default**
- Firewall must allow **port 22**

Example:

```
Client → Internet → Port 22 → SSH Server
```

---

# 4. Connecting to a Remote Server

### Basic Connection

```
ssh root@168.144.21.242
```

Example output:

```
Welcome to Ubuntu 24.04.3 LTS
System information:
Memory usage: 39%
IPv4 address: 168.144.21.242
```

Exit connection:

```
exit
```

---

# 5. Using a Specific SSH Key

Normally SSH checks **default key location**:

```
~/.ssh/id_rsa
```

If you have **multiple key pairs**, SSH may use the wrong one.

So you must specify the key manually:

```
ssh -i ~/.ssh/id_rsa root@168.144.21.242
```

- `i` = identity file (private key)

---

# 6. Secure File Transfer with SCP

SSH also allows **secure file copying** using **SCP (Secure Copy Protocol)**.

Example:

```
scp test.sh root@168.144.21.242:/root
```

Meaning:

```
scp <file> <user>@<server>:<destination>
```

Example result:

```
test.sh   100% 49B
```

---

# 7. Verifying File on Remote Server

Login to server:

```
ssh root@168.144.21.242
```

Check file:

```
ls
```

Example output:

```
test.sh
```

Check permissions:

```
ls -l
```

```
-rw-r--r-- 1 root root 49 Mar 6 test.sh
```

Make file executable:

```
chmod u+x test.sh
```

Run script:

```
./test.sh
```

Output:

```
i am remote server connected
```

---

# 8. Important SSH Key Rule

If you have **multiple SSH keys**, always specify the correct key:

```
ssh -i ~/.ssh/key_name user@server
```

Otherwise SSH will try **default key** and connection may fail.

---

# 9. Summary

SSH provides:

- Secure remote access
- Encrypted communication
- Secure authentication
- Secure file transfer

Common SSH tools:

| Tool | Purpose |
| --- | --- |
| ssh | connect to server |
| ssh-keygen | generate keys |
| scp | copy files securely |
| chmod | change file permissions |