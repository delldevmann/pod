import streamlit as st
from fastapi import FastAPI
from threading import Thread
import uvicorn

# Initialize Streamlit app configuration
st.set_page_config(layout="wide", page_title="Simple C2 Dashboard")

# FastAPI app setup
app = FastAPI()

# Sidebar - App title and master information
master_url = "https://m-dashboardpy-app9jfrumktgxrf359vu6t6.streamlit.app/"
master_ip = "10.12.175.191"
st.sidebar.title("Simple Command & Control (C2) Dashboard")
st.sidebar.write("Master Node URL:")
st.sidebar.write(master_url)
st.sidebar.write("Master Node IP Address:")
st.sidebar.write(master_ip)

# Placeholder for connected agents
targets = {}

# FastAPI endpoint to register agents
@app.post("/register_agent/")
async def register_agent(agent_id: str):
    if agent_id not in targets:
        targets[agent_id] = "Connected"
        st.session_state['logs'] += f"\n[+] Agent {agent_id} connected"
    return {"message": f"Agent {agent_id} registered successfully"}

# FastAPI endpoint to receive command output from agent
@app.post("/command_response/")
async def command_response(agent_id: str, response: str):
    st.session_state['logs'] += f"\n[+] Response from Agent {agent_id}: {response}"
    return {"message": "Response received successfully"}

# Run FastAPI server in a separate thread
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

Thread(target=run_fastapi, daemon=True).start()

# Streamlit UI for connected agents and command execution
col1, col2 = st.columns([1, 2])

# Column 1 - Connected Agents
with col1:
    st.subheader("Connected Agents")
    if targets:
        for agent_id in targets:
            st.write(f"Agent: {agent_id}")
    else:
        st.write("No agents connected.")

# Column 2 - Command Execution
with col2:
    st.subheader("Command Execution")
    if targets:
        selected_agent = st.selectbox("Select Agent", options=list(targets.keys()))
        command = st.text_input("Enter Command to Execute")
        if st.button("Send Command"):
            st.session_state['logs'] += f"\n[+] Command sent to {selected_agent}: {command}"
            # Here you would implement the logic to send command to agent (e.g., using an HTTP request)

# Display Logs
st.subheader("Logs")
if 'logs' not in st.session_state:
    st.session_state['logs'] = "[INFO] Starting Simple C2 Server..."
st.text_area("Logs", st.session_state['logs'], height=300)
