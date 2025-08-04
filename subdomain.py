import subprocess
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Telegram Bot Configuration
TELEGRAM_TOKEN = "<Your_Telegram_token>"
TELEGRAM_CHAT_ID = "<Your_chat_id>"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[!] Telegram Error: {e}")


def get_subdomains(domain):
    try:
        result = subprocess.run(
            ["subfinder", "-silent", "-d", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        subdomains = result.stdout.strip().split("\n")
        return list(set(subdomains))
    except Exception as e:
        print(f"[!] subfinder failed: {e}")
        return []


def is_active(subdomain):
    try:
        for scheme in ["http://", "https://"]:
            url = scheme + subdomain
            response = requests.get(url, timeout=3)
            if response.status_code < 500:
                return subdomain
    except:
        return None


def find_active_subdomains(subdomains):
    active = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(is_active, subdomains)
        for res in results:
            if res:
                active.append(res)
    return active


def main():
    domain = input("Enter the domain (e.g. example.com): ").strip()

    send_telegram_message(f"🔎 Starting Subdomain Scan for: {domain}")

    subdomains = get_subdomains(domain)
    if not subdomains:
        send_telegram_message("⚠️ No subdomains found or error occurred.")
        return

    send_telegram_message(f"✅ Found {len(subdomains)} subdomains. Checking for live ones...")

    active_subdomains = find_active_subdomains(subdomains)

    if not active_subdomains:
        send_telegram_message("❌ No active subdomains found.")
        return

    result = "🟢 Active Subdomains:\n" + "\n".join(active_subdomains)

    # Split if too long
    if len(result) > 4096:
        for i in range(0, len(result), 4000):
            send_telegram_message(result[i:i + 4000])
    else:
        send_telegram_message(result)

    print("[✓] Done. Results sent to Telegram.")


if __name__ == "__main__":
    main()
