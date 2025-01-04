#!/usr/bin/env python3

import socket
import threading

# Define the host and port for the server
HOST = '0.0.0.0'  # Localhost
PORT = 50123        # Port to listen on

# so far only listening, interaction later

def handle_client(client_socket, address):
    """
    Handles communication with a connected client.
    """
    print(f"[NEW CONNECTION] {address} connected.")
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # Client disconnected

            print(f"[RECEIVED] From {address}: {data}")

            i = 0
            msg_len = int.from_bytes(data[i:(i := i+2)], byteorder="little")
            print(f"{msg_len=} ?= {len(data)}")

            if i > len(data):
                print("data too short")
                continue

            tst = int.from_bytes(data[i:(i := i+3)], byteorder="little")
            print(f"{tst=} ?= {0x245}")

            if i > len(data):
                print("data too short")
                continue

            tst = int.from_bytes(data[i:(i := i+8)], byteorder="little")
            print(f"counter maybe? {tst=}")

            if i > len(data):
                print("data too short")
                continue

            tst = int.from_bytes(data[i:(i := i+4)], byteorder="little")
            print(f"static 0x33? {tst=} ?= {0x33}")

            if i > len(data):
                print("data too short")
                continue

            tst = int.from_bytes(data[i:(i := i+4)], byteorder="little")
            print(f"idk? {tst=}")

            if i > len(data):
                print("data too short")
                continue

            tst = data[i:]
            print(f"e2? {tst=} ?= E2[...]")

            # Parse the received message
            response = parse_message(data)

            # Send a response back to the client
            client_socket.sendall(response)
    except Exception as e:
        print(f"[ERROR] {address}: {e}")
    finally:
        print(f"[DISCONNECTED] {address}")
        client_socket.close()

def parse_message(message):
    """
    Parses the incoming message and returns an appropriate response.
    """
    try:
        # Example: Check if the message is a specific command
        if message.lower() == "hello":
            return "Hello! How can I help you?"
        elif message.lower() == "status":
            return "Server is running fine."
        else:
            return f"Received: {message}"
    except Exception as e:
        return f"Error parsing message: {e}"

def start_server():
    """
    Starts the TCP server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Listen for up to 5 connections
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    try:
        while True:
            # Accept a new client connection
            client_socket, client_address = server.accept()
            # Handle the client in a new thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server is shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()