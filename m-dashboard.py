import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Simple C2 Master Node Dashboard")

# Flask server URL
flask_url = "http://localhost:5000"  # Update with the public URL of your Flask server

st.sidebar.title("Simple Command & Control (C2) Dashboard")
st.sidebar.write("Master Node (via Flask)")

# Fetch connected agents
if st.button("Refresh Connected Agents"):
    try:
        response = requests.get(f"{flask_url}/agents")
        if response.status_code == 200:
            agents = response.json()
            if agents:
                for agent_id, info in agents.items():
                    st.write(f"Agent: {agent_id}, Last Seen: {info['last_seen']}")
            else:
                st.write("No agents connected.")
        else:
            st.write("Failed to retrieve agents.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Flask server: {e}")
