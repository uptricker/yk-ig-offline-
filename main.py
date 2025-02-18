import time
import threading
from instagrapi import Client
from flask import Flask, request, jsonify

app = Flask(__name__)

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

# Endpoint to start the Instagram message sending
@app.route('/send_messages', methods=['POST'])
def start_message_sending():
    try:
        # Read input files
        username = read_file('username.txt')[0]
        password = read_file('password.txt')[0]
        target_username = read_file('target.txt')[0]
        messages = read_file('messages.txt')
        delay = int(read_file('delay.txt')[0]) if read_file('delay.txt') else 2
        repeat_time = int(read_file('repeattime.txt')[0]) if read_file('repeattime.txt') else 1

        if not username or not password or not target_username or not messages:
            return jsonify({"error": "Missing input data. Check your files."}), 400

        # Login to Instagram
        client = instagram_login(username, password)
        if not client:
            return jsonify({"error": "Login failed. Check your credentials."}), 500

        # Start a new thread to send messages
        message_thread = threading.Thread(target=send_message, args=(client, target_username, messages, delay, repeat_time))
        message_thread.start()
        message_thread.join()

        return jsonify({"message": "Messages sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    # Set the port where the server will run
    app.run(host='0.0.0.0', port=5000)
        
