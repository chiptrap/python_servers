"""
Bricen Chitty
03/09/2025
Assignment: tcp_client
Version 3

Description:
-----------
A TCP client that connects to a server, sends multiple messages,
and receives MD5 hash responses for each message sent.

This client sends 10 predefined text messages to the server and displays
the MD5 hash digest that the server computes and returns.

Network Details:
--------------
- Connects to server at 127.0.0.1:5555 by default
- Uses TCP (SOCK_STREAM) for reliable data transmission
"""

import socket

def main():
    """
    Main client function: connect to server, send messages, receive responses.
    Handles connection errors and ensures socket cleanup.
    """
    # IP address or hostname of the server
    # Use 127.0.0.1 if the server is on the same machine.
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 5555
    
    # Create a socket object
    # AF_INET = IPv4, SOCK_STREAM = TCP protocol
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[*] Connecting to {SERVER_IP}:{SERVER_PORT}")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        # Prepare 10 different messages
        messages = [
            "First message: Hello, server!",
            "Second message: How are you?",
            "Third message: I am fine.",
            "Fourth message: What is your name?",
            "Fifth message: My name is Client.",
            "Sixth message: What is the time?",
            "Seventh message: It is 12:00 PM.",
            "Eighth message: What is the date?",
            "Ninth message: Today is Monday.",
            "Tenth message: Goodbye!"
        ]
        
        # Send each message, then receive and display the server's MD5 response
        for i, msg in enumerate(messages, start=1):
            data_to_send = msg.encode()  # Convert string to bytes for transmission
            
            print(f"\n[->] Sending message {i}: {msg}")
            client_socket.sendall(data_to_send)  # Send the message reliably
            
            # Receive the MD5 digest (up to 1024 bytes)
            response = client_socket.recv(1024)
            if not response:
                # Empty response indicates server closed connection
                print("[!] No response received (server may have closed).")
                break
            
            # Decode bytes to string and display the hash
            md5_hash = response.decode()
            print(f"[<-] Received MD5 hash: {md5_hash}")
            
        print("\n[*] All messages sent.")
        print("[*] Closing connection.")
        
    except ConnectionRefusedError:
        # This happens when no server is listening at the specified IP:PORT
        print(f"[!] Connection refused. Could not connect to {SERVER_IP}:{SERVER_PORT}.")
        print("[!] Is the server running?")
    except socket.timeout:
        # If we set a timeout and it expires
        print("[!] Connection timed out. Server might be slow or unreachable.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"[!] An error occurred: {e}")
    finally:
        # Always close the socket, even if there's an error
        client_socket.close()
        
if __name__ == "__main__":
    main()