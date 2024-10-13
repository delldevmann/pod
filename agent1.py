import streamlit as st
import requests
import time

# Set up the Streamlit page
st.set_page_config(layout="wide", page_title="Simple C2 Agent Node")

# Agent ID for this specific agent
agent_id = "agent-001"  # Each agent should have a unique ID

# Master node URL
master_url = "https://m-dashboardpy-app9jfrumktgxrf359vu6t6.streamlit.app/"  # Replace with your deployed master node URL

# Polling the Master Node to Update Status
if st.button("Update Master Node"):
    # Simulate sending status update to the master node
    try:
        response = requests.get(f"{master_url}?agent_id={agent_id}")
        if response.status_code == 200:
            st.write("Agent update successful.")
        else:
            st.write(f"Failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating master node: {e}")

# Display log information
st.write(f"Agent ID: {agent_id}")
st.write("Sending update to Master Node...")
