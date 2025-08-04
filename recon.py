import os
import subprocess
import xml.etree.ElementTree as ET
import json
import requests
from datetime import datetime

# --- Configuration ---
NMAP_OUTPUT_FILE = "scan_output.xml"

# Telegram Bot Setup
TELEGRAM_TOKEN = "<Your_telegram_token>"
TELEGRAM_CHAT_ID = "<Your_telegram_chat_id>"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"[!] Telegram error: {response.text}")
    except Exception as e:
        print(f"[!] Telegram exception: {e}")

def run_nmap(target):
    print(f"[*] Running Nmap quick scan on {target} (ports 20–1024)...")
    cmd = f"nmap -T4 -sS -p 20-1024 -oX {NMAP_OUTPUT_FILE} {target}"
    subprocess.run(cmd, shell=True)

def parse_nmap_xml():
    ports_found = {}
    try:
        tree = ET.parse(NMAP_OUTPUT_FILE)
        root = tree.getroot()
    except Exception as e:
        send_telegram_alert(f"[!] Failed to parse Nmap XML output: {e}")
        return {}

    for host in root.findall("host"):
        ip_elem = host.find("address")
        if ip_elem is None:
            continue
        ip = ip_elem.get("addr")
        ports_found[ip] = []

        for port in host.findall("ports/port"):
            port_id = port.get("portid")
            state = port.find("state").get("state")
            if state == "open":
                ports_found[ip].append(int(port_id))
    return ports_found

def main():
    target = input("Enter IP address or domain: ").strip()

    run_nmap(target)

    if not os.path.exists(NMAP_OUTPUT_FILE):
        print(f"[!] Nmap output file '{NMAP_OUTPUT_FILE}' not found.")
        send_telegram_alert("[!] Nmap scan failed. Output file not found.")
        return

    open_ports = parse_nmap_xml()

    report = f"📡 Scan Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n"
    report += json.dumps(open_ports, indent=2)

    print(report)

    # Telegram message size limit is 4096 characters
    if len(report) > 4096:
        chunks = [report[i:i+4000] for i in range(0, len(report), 4000)]
        for part in chunks:
            send_telegram_alert(part)
    else:
        send_telegram_alert(report)

    print("[✓] Scan complete. Results sent to Telegram.")

if __name__ == "__main__":
    main()
