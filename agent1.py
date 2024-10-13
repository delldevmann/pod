import streamlit as st
import requests
import socket
import time

# Set up the Streamlit page
st.set_page_config(layout="wide", page_title="Simple C2 Agent Node")

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

# Agent ID for this specific agent
agent_id = "agent-001"  # Each agent should have a unique ID
agent_ip = get_actual_ip()

# Master node URL
master_url = "https://m-dashboardpy-app9jfrumktgxrf359vu6t6.streamlit.app/"  # Replace with your deployed master node URL

# Sidebar to show agent information
st.sidebar.title("Agent Information")
st.sidebar.write("Agent ID:", agent_id)
st.sidebar.write("Agent IP Address:", agent_ip)

# Agent Registration and Polling for Commands
if st.button("Poll Master for Commands"):
    # Register and Poll master node using query parameters
    try:
        response = requests.get(f"{master_url}?agent_id={agent_id}")
        if response.status_code == 200:
            st.write("Polling successful.")
        else:
            st.write(f"Failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to master node: {e}")

# Display log information
st.write(f"Agent ID: {agent_id}")
st.write("Polling Master Node for Commands...")
