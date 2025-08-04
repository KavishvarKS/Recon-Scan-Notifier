# 🔍 Telegram-Integrated Nmap Quick Scanner

## 📜 Description

This Python script performs a quick **SYN scan** (`-sS`) on the first 1000 TCP ports (20–1024) of a target host using **Nmap** and sends the results directly to a **Telegram bot**.

It’s perfect for simple reconnaissance use cases where you want to quickly check for open ports on a system and be notified remotely via Telegram.

---

## 🚀 Features

* Uses `nmap` to perform a fast TCP port scan
* Outputs results in XML and parses them using Python
* Sends results as JSON via **Telegram Bot API**
* Automatically splits large messages to respect Telegram’s character limit
* Includes timestamped scan reports
* Lightweight and easy to extend

---

## 🧠 How It Works (Script Breakdown)

### 1. **Configuration**

```python
NMAP_OUTPUT_FILE = "scan_output.xml"
TELEGRAM_TOKEN = "<your_bot_token>"
TELEGRAM_CHAT_ID = "<your_chat_id>"
```

Set your bot’s token and chat ID for Telegram alerts.

---

### 2. **`send_telegram_alert()`**

Sends a message to your Telegram using a POST request to:

```
https://api.telegram.org/bot<token>/sendMessage
```

---

### 3. **`run_nmap(target)`**

Runs a fast SYN scan on ports 20–1024:

```bash
nmap -T4 -sS -p 20-1024 -oX scan_output.xml <target>
```

* `-T4`: Aggressive timing (faster)
* `-sS`: Stealth SYN scan
* `-p 20-1024`: Scan common ports
* `-oX`: Output in XML format (so Python can parse it)

---

### 4. **`parse_nmap_xml()`**

Parses the generated `scan_output.xml` file to extract:

* IP address of the scanned host
* List of **open ports**

Returns a dictionary like:

```json
{
  "192.168.1.1": [22, 80, 443]
}
```

---

### 5. **`main()`**

* Prompts the user for a target (IP or domain)
* Runs the scan and parses the output
* Formats the results into a readable string with timestamps
* Sends the result to Telegram (in chunks if necessary)

---

## 📦 Example Output (on Telegram)

```
📡 Scan Report (2025-08-03 14:30:00):
{
  "scanme.nmap.org": [22, 80]
}
```

---

## ✅ Requirements

* Python 3.x
* `nmap` installed and available in your system path
* An active **Telegram bot** and **chat ID**

---

## 🔐 Security Warning

**Never share your real Telegram bot token or chat ID publicly.**
Always use environment variables or `.env` files in production.

