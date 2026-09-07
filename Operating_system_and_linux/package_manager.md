# 📦 Linux Package Management – Review Notes

## 1️⃣ What Is a Package Manager?

A **package manager** is a tool that:

- Installs software packages
- Removes/uninstalls software
- Upgrades software
- Manages dependencies (other packages required to run a program)
- Keeps track of installed files and versions

It ensures software is installed in the correct locations and works properly with the system.

---

# 🐧 Package Management in Ubuntu

Ubuntu is a **Debian-based** distribution and primarily uses:

## 🔹 1. APT (Advanced Package Tool)

**APT** = Advanced Package Tool

It is the default package manager in Ubuntu.

### What APT Does:

- Installs packages from official repositories
- Automatically installs required dependencies
- Removes packages cleanly
- Updates package lists and upgrades software

### Important Commands:

```
sudo apt update# Refresh package list
sudo apt upgrade# Upgrade installed packages
sudo apt install pkg# Install a package
sudo apt remove pkg# Remove a package
```

sudo apt autoremove  to remove unsed packages

### Where APT Gets Packages From

APT downloads software from repositories listed in:

```
/etc/apt/sources.list
/etc/apt/sources.list.d/
```

Ubuntu systems are connected to official Ubuntu repositories by default.

---

## 🔹 2. Snap Package Manager

Ubuntu also supports **Snap**, developed by

Canonical

A **Snap package**:

- Is a self-contained bundle
- Includes the application AND all its dependencies
- Works across many Linux distributions

### Snap Advantages:

- Universal across many Linux distros
- Automatic updates
- More isolated (sandboxed)

### Snap Disadvantages:

- Larger installation size (because dependencies are included)
- Can be slightly slower to start

### Install a Snap:

```
sudo snap install package-name
```

---

# 🔍 APT vs Snap (Important Comparison)

| Feature | APT | Snap |
| --- | --- | --- |
| Dependency Handling | Shared between apps | Included inside package |
| Disk Usage | Smaller | Larger |
| Updates | Manual (apt upgrade) | Automatic |
| Cross-Distro Support | Mostly Debian-based | Universal |
| Speed | Faster startup | Slightly slower startup |
|  |  |  |

### Key Concept:

With **APT**, dependencies are shared.

If two applications need the same library, it is installed only once.

With **Snap**, each package contains its own dependencies.

This increases size but improves compatibility and isolation.

---

# 🔹 3. Adding Repositories

Sometimes a package is not available in default Ubuntu repositories.

In that case, you can:

### ➤ Add a New Repository

Repositories are software sources stored in:

```
/etc/apt/sources.list
```

After adding a repository, run:

```
sudo apt update
```

So APT refreshes the package list.

---

## 🔹 PPA (Personal Package Archive)

PPA = Personal Package Archive

A PPA allows developers to:

- Create and maintain their own software repository
- Provide newer or custom versions of software

PPAs are commonly hosted on

Launchpad

### Add a PPA:

```
sudo add-apt-repository ppa:name/ppa
sudo apt update
```

### ⚠️ Important:

- PPAs are not officially verified by Ubuntu.
- Use only trusted PPAs.
- There is some security risk.

---

# 🖥 Ubuntu Software Center

Ubuntu also provides a graphical interface:

## ➤ Ubuntu Software

It allows users to:

- Install applications visually
- Manage Snap and APT packages
- View reviews and descriptions

It works on top of APT and Snap.

---

# 🏷 Types of Linux Distributions (Important for Exams)

There are two major distribution families:

---

## 🔹 1. Debian-Based Distributions

Examples:

- Ubuntu
- Linux Mint
- Debian

Package Manager:

- APT
- apt-get
- dpkg (low-level tool)

---

## 🔹 2. Red Hat-Based Distributions

Examples:

- RHEL
- CentOS
- Fedora

Package Managers:

- YUM (older)
- DNF (modern replacement for YUM)
- RPM (low-level tool)

---

# 📌 Final Summary (Exam Quick Review)

- A **package manager** installs, removes, and manages software.
- Ubuntu uses **APT** as its main package manager.
- **Snap** packages are self-contained and universal.
- APT shares dependencies; Snap bundles them.
- Repositories are listed in `/etc/apt/sources.list`.
- PPAs allow third-party repositories but must be used carefully.
- Debian-based systems use APT.
- Red Hat-based systems use YUM/DNF.