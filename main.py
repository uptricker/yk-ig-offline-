import time
import threading
from instagrapi import Client

# Function to login to Instagram
def instagram_login(username, password):
    try:
        client = Client()
        client.login(username, password)
        print("[SUCCESS] Logged into Instagram!")
        return client
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None

# Function to send messages
def send_message(client, target_username, messages, delay, repeat_time):
    try:
        user_id = client.user_id_from_username(target_username)

        for _ in range(repeat_time):
            for index, message in enumerate(messages):
                client.direct_send(message, [user_id])
                print(f"[SUCCESS] Sent message {index + 1} to {target_username}: {message}")
                time.sleep(delay)
    except Exception as e:
        print(f"[ERROR] Failed to send messages: {e}")

# Function to read a file and return the content
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        print(f"[ERROR] Failed to read file {file_path}: {e}")
        return []

# Main function
def main():
    # Read input files
    username = read_file('username.txt')[0]
    password = read_file('password.txt')[0]
    target_username = read_file('target.txt')[0]
    messages = read_file('messages.txt')
    delay = int(read_file('delay.txt')[0]) if read_file('delay.txt') else 2
    repeat_time = int(read_file('repeattime.txt')[0]) if read_file('repeattime.txt') else 1

    if not username or not password or not target_username or not messages:
        print("[ERROR] Missing input data. Check your files.")
        return

    # Login to Instagram
    client = instagram_login(username, password)
    if not client:
        return

    # Start a new thread to send messages
    message_thread = threading.Thread(target=send_message, args=(client, target_username, messages, delay, repeat_time))
    message_thread.start()
    message_thread.join()

if __name__ == "__main__":
    main()
    