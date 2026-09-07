# Networking Basics

## 1. What is an IP Address?

**IP (Internet Protocol)** is a unique address assigned to a device on a network.

### IPv4

- IPv4 is a **32-bit address**
- Divided into **4 sections (octets)**
- Each octet contains **8 bits**
- Total = **8 × 4 = 32 bits**

Example:

```
192.168.1.10
```

Binary representation:

```
11000000.10101000.00000001.00001010
```

### Bit Values

A bit can be:

```
0 or 1
```

An octet ranges from:

```
00000000 = 0
11111111 = 255
```

Therefore an IPv4 address range is:

```
0.0.0.0  →  255.255.255.255
```

---

# 2. LAN (Local Area Network)

**LAN (Local Area Network)** is a collection of devices connected within a small physical area.

Examples:

- Home network
- Office network
- College lab
- Data center rack

### Characteristics

- Devices have unique IP addresses.
- Devices communicate using their IP addresses.
- Communication is usually very fast.
- A switch is used to connect devices.

Example:

```
Laptop      192.168.1.10
Server      192.168.1.20
Printer     192.168.1.30
```

All are part of the same LAN.

---

# 3. Switch

A **switch** connects devices inside a LAN.

### Responsibilities

- Connects devices in the local network.
- Forwards data to the correct device.
- Uses MAC addresses to identify devices.

Example:

```
Laptop ──┐
          │
Server ─ Switch
          │
Printer ─┘
```

### Important Point

Switch works only inside the local network (LAN).

---

# 4. Router

A **router** connects one network to another network.

Usually:

```
LAN → Router → Internet
```

### Responsibilities

- Connects LAN to WAN.
- Routes traffic between networks.
- Acts as the default gateway.

Example:

```
Laptop
   │
Switch
   │
Router
   │
Internet
```

---

# 5. Gateway

A **gateway** is the exit point from a local network.

Usually the gateway IP is the router's IP.

Example:

```
Laptop IP  : 192.168.1.10
Gateway IP : 192.168.1.1
```

When the laptop wants to access Google, it sends traffic to:

```
192.168.1.1
```

(router/gateway)

---

# 6. WAN (Wide Area Network)

**WAN (Wide Area Network)** connects multiple LANs over large distances.

Examples:

- Internet
- Corporate networks between cities
- Cloud networks

Example:

```
Office LAN (Delhi)
        │
      Internet
        │
Office LAN (Mumbai)
```

---

# 7. Private IP Address Ranges

Private IPs are used inside organizations and homes.

They are **not directly accessible from the Internet**.

### Class A

```
10.0.0.0 - 10.255.255.255
```

Very large network.

---

### Class B

```
172.16.0.0 - 172.31.255.255
```

Medium-sized network.

---

### Class C

```
192.168.0.0 - 192.168.255.255
```

Small networks (home and offices).

---

# 8. What is a Subnet?

A **subnet (sub-network)** is a smaller network created from a larger network.

Purpose:

- Better organization
- Better security
- Reduced broadcast traffic

Example:

Network:

```
192.168.1.0/24
```

Can be divided into:

```
192.168.1.0/25
192.168.1.128/25
```

Now we have two smaller networks.

### Why Subnetting?

Suppose a company has:

```
HR Department
Development Team
Testing Team
```

Instead of putting everyone in one network, we create:

```
HR      → 192.168.1.0/24
Dev     → 192.168.2.0/24
QA      → 192.168.3.0/24
```

This improves security and network management.

---

# 9. What is NAT?

**NAT (Network Address Translation)** converts private IP addresses into public IP addresses.

### Why NAT is Needed

Private IPs cannot access the Internet directly.

Example:

```
Laptop : 192.168.1.10
```

Google does not know this IP.

Router performs NAT:

```
192.168.1.10
       ↓
49.x.x.x (Public IP)
```

Now communication with the Internet is possible.

### Benefits of NAT

1. Saves public IP addresses.
2. Hides internal network structure.
3. Provides an additional layer of security.
4. Allows thousands of devices to share one public IP.

Example:

```
Laptop
Mobile
TV
Server
   ↓
Router (NAT)
   ↓
Single Public IP
   ↓
Internet
```

---

# Company A

```
Laptop          192.168.1.10
Server          192.168.1.20
Router
Public IP = 103.25.40.5
```

# Company B

```
Laptop          192.168.1.10
Printer         192.168.1.20
Router
Public IP = 89.150.12.9
```

Notice something?

Both companies are using

```
192.168.1.10
```

inside their own LAN.

Is this a problem?

**No.**

Because **private IP addresses only exist inside their own LAN.**

# 10. Firewall

A **firewall** controls incoming and outgoing network traffic.

Think of it as a security guard.

### Responsibilities

- Allow trusted traffic.
- Block unwanted traffic.
- Protect systems from unauthorized access.

Example:

```
Allow:
Port 22  (SSH)
Port 80  (HTTP)
Port 443 (HTTPS)

Block:
Everything else
```

---

# 11. Ports

A **port** identifies a specific service running on a device.

IP identifies the machine.

Port identifies the application.

Example:

```
192.168.1.10:22
```

- IP → Machine
- Port → SSH Service

### Common Ports

| Port | Service |
| --- | --- |
| 22 | SSH |
| 21 | FTP |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 8080 | Application Servers |

### Example

```
192.168.1.20:80
```

Web server running on port 80.

---

# 12. DNS (Domain Name System)

DNS translates domain names into IP addresses.

Humans remember:

```
google.com
```

Computers communicate using:

```
142.x.x.x
```

DNS performs the translation.

### Flow

```
Browser
   ↓
DNS Server
   ↓
Returns IP Address
   ↓
Connect to Website
```

Example:

```
google.com
      ↓
142.250.x.x
```

### Why DNS?

Without DNS, we would need to remember IP addresses for every website.

---

# Complete Network Flow (Interview Question)

When you open:

```
https://google.com
```

Flow:

```
1. Browser requests google.com

2. DNS converts google.com → IP

3. Request goes to Gateway (Router)

4. Router performs NAT

5. Traffic reaches Internet

6. Google's server responds

7. Response comes back through Router

8. Router sends data to your device
```

### One-Line Definitions (Interview Revision)

- **IP Address** → Unique address of a device on a network.
- **LAN** → Local network connecting nearby devices.
- **Switch** → Connects devices within a LAN.
- **Router** → Connects different networks.
- **Gateway** → Exit point of a network.
- **WAN** → Large network connecting multiple LANs.
- **Subnet** → Smaller network created from a larger network.
- **NAT** → Converts private IPs to public IPs.
- **Firewall** → Controls allowed and blocked traffic.
- **Port** → Identifies a specific service/application.
- **DNS** → Converts domain names into IP addresses.

These are exactly the networking fundamentals that freque

| Command | Purpose | When to Use | Example |
| --- | --- | --- | --- |
| `ip addr` or `ip a` | Show network interfaces and IP addresses | Check whether the server has an IP address and which interface is being used | `ip addr` |
| `ip route` | Show routing table and default gateway | Verify the default gateway and routing if the server cannot reach another network or the Internet | `ip route` |
| `ss -tulpn` | Show listening ports and processes | Check if an application (Nginx, SSH, PostgreSQL, etc.) is actually listening on the expected port | `ss -tulpn` |
| `dig google.com` | Perform a DNS lookup | Verify DNS resolution and troubleshoot domain name issues | `dig google.com` |
| `ping 8.8.8.8` | Test basic network connectivity | Check if the server can reach another host or the Internet | `ping 8.8.8.8` |
| `traceroute google.com` | Show the path packets take | Identify where packets are being delayed or dropped | `traceroute google.com` |
| `curl -v https://google.com` | Test HTTP/HTTPS connectivity | Verify that a web server or API is reachable and responding correctly | `curl -v https://google.com` |
| `nc -vz host 443` | Test if a TCP port is reachable | Check whether a specific port is open and accepting connections | `nc -vz server-ip 22` |
| `hostname -I` | Display the machine's IP address(s) | Quickly get the server's IP without extra interface details | `hostname -I` |
| `hostname` | Show the system hostname | Verify the machine's hostname | `hostname` |