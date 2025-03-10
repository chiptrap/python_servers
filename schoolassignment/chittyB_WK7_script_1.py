"""
Bricen Chitty
03/09/2025
Assignment: tcp_server
Version 5

Description:
-----------
A multi-threaded TCP server that accepts client connections, computes MD5 hashes
of data received from clients, and returns the hash digests to the clients.

Key Features:
- Multi-client support using threads
- MD5 hash computation
- Error handling and clean shutdown

Architecture:
-----------
The server follows a main thread + worker threads pattern:
1. Main thread: Binds to a socket, listens for connections, and spawns worker threads
2. Worker threads: Handle individual client connections and process their data

Network Details:
--------------
- Binds to all network interfaces (0.0.0.0)
- Default port: 5555
- Uses TCP (SOCK_STREAM) for reliable data transmission
"""

import socket  # Network communication
import threading  # Multi-client handling
import hashlib  # MD5 hash computation

# Network configuration 
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5555  # TCP port to listen on

def handle_client(client_socket, address):
    """
    Process client connections in a separate thread.
    Receives data, computes MD5 hash, and sends hash back.
    """
    
    print(f"[*] Accepted connection from {client_socket.getpeername()}")
    
    # Process client data until disconnect
    while True:
        try:
            # Receive data from client
            data = client_socket.recv(1024)  # 1KB buffer size
            
            if not data:
                # Empty data means client disconnected
                print(f"[*] Client at {address} disconnected")
                break
            
            # Calculate MD5 hash of received data
            md5_hash = hashlib.md5(data)
            digest = md5_hash.hexdigest().encode()
            
            # Send hash back to client
            client_socket.send(digest)
            
        except ConnectionResetError:
            # Client abruptly disconnected
            print(f"[*] Connection reset by client at {address}")
            break
        except Exception as e:
            print(f"[!] Error with {address}: {e}")
            break
        
    # Clean up resources
    client_socket.close()
    print(f"[*] Closed connection from {address}")

def main():
    """
    Main server function: create socket, bind, listen for connections,
    and spawn client handler threads.
    """
    
    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind to specified host/port
        server.bind((HOST, PORT))
    except OSError as e:
        print(f"[!] Could not bind to {HOST}:{PORT}: {e}")
        print("[!] Check for other servers or change ports.")
        return
    
    # Listen with backlog queue of 5
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")
    print("[*] Press Ctrl+C to stop the server")
    
    # Accept and process connections
    while True:
        try:
            # Wait for client connection
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr}")
            
            # Create thread to handle client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr),
            )
            client_thread.start()
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n[*] User requested an exit.")
            server.close()
            break
        except Exception as e:
            print(f"[!] Error in main loop: {e}")
            server.close()
            break
    
    print("[*] Server terminated.")

if __name__ == "__main__":
    main()