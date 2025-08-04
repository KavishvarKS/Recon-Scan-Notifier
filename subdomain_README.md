---

# 🌐 Telegram-Based Active Subdomain Scanner

## 📜 Description

This Python script uses **Subfinder** to discover subdomains of a target domain and checks which ones are **actively responding** (via HTTP/HTTPS). The results are automatically sent to your **Telegram bot**.

---

## 🚀 Features

* Uses [`subfinder`](https://github.com/projectdiscovery/subfinder) for passive subdomain enumeration
* Validates which subdomains are **alive** (HTTP/HTTPS)
* Parallel checking using Python's `ThreadPoolExecutor` for speed
* Sends progress and final results to Telegram
* Handles long message outputs by splitting into chunks

---

## 🧠 Script Breakdown

### 1. **Configuration**

```python
TELEGRAM_TOKEN = "<your_bot_token>"
TELEGRAM_CHAT_ID = "<your_chat_id>"
```

* Replace these with your own Telegram credentials.

---

### 2. **`send_telegram_message()`**

Sends a message to your Telegram bot using the **Telegram Bot API**:

```
https://api.telegram.org/bot<token>/sendMessage
```

---

### 3. **`get_subdomains(domain)`**

Uses **Subfinder** to get a list of subdomains:

```bash
subfinder -silent -d example.com
```

Returns the results as a Python list.

---

### 4. **`is_active(subdomain)`**

Checks if the subdomain is reachable via:

* `http://subdomain`
* `https://subdomain`

Sends a request to each. If the subdomain responds with a non-5xx status, it’s considered **alive**.

---

### 5. **`find_active_subdomains(subdomains)`**

Uses a thread pool (`max_workers=20`) to **concurrently** check all subdomains using the `is_active()` function.

---

### 6. **`main()` Function Flow**

1. Prompts user for the domain name
2. Sends a "starting scan" message to Telegram
3. Collects subdomains using Subfinder
4. Sends number of found subdomains to Telegram
5. Checks which subdomains are **alive**
6. Sends the list of live subdomains to Telegram (in chunks if needed)

---

## 📦 Example Output (Telegram Bot)

```
🔎 Starting Subdomain Scan for: tesla.com
✅ Found 213 subdomains. Checking for live ones...
🟢 Active Subdomains:
https://shop.tesla.com
https://energy.tesla.com
https://model3.tesla.com
...
```

---

## ✅ Requirements

* Python 3.x
* [`subfinder`](https://github.com/projectdiscovery/subfinder) installed and in `$PATH`
* Internet access for HTTP requests
* Telegram bot and chat ID setup

---

## 🔐 Security Reminder

🔒 **Do not share your Telegram token or chat ID** publicly. Use `.env` or config files if possible.

---
