# Honeypot
# Multi-Service Honeypot

A lightweight honeypot that exposes **fake SSH, FTP, and HTTP services** to capture attacker interactions such as connection attempts, credentials, and commands.  
This tool runs multiple sockets concurrently and logs all activity to the terminal.

---

## ✨ Features

- Fake **SSH** server (port 2222)
- Fake **FTP** server (port 2121)
- Fake **HTTP** server (port 8080)
- Logs:
  - IP address of client
  - Received username/password
  - Commands or requests sent by attacker
- Multi-threaded, handles multiple connections
- Very lightweight (pure Python)

---

## 🏗️ Architecture

Each service runs in its own thread:

- `ssh_server()`  
- `ftp_server()`  
- `http_server()`  

Common behavior:

1. Accept connection
2. Prompt for username & password
3. Log credentials
4. Accept mock commands/requests
5. Close connection or persist until attacker disconnects

---

## 🔧 Installation

Clone or download the repo:

```bash
git clone https://github.com/yourname/honeypot.git
cd honeypot
#Install dependencies (optional, only rich)
pip install -r requirements.txt

#Usage

Run the honeypot:

python3 main.py


Expected output:

[+] http running on 0.0.0.0:8080
[+] ftp  running on 0.0.0.0:2121
[+] ssh  running on 0.0.0.0:2222


When an attacker connects, you’ll see logs like:

[SSH] Connection from 192.168.1.10
[SSH] Username: root
[SSH] Password: 12345
[SSH] Command: whoami
