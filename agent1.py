import requests
import time

# Agent Implementation
def agent(master_url):
    agent_id = "agent-001"  # Unique ID for the agent

    # Register with the master
    registration_url = f"{master_url}/register_agent/"
    response = requests.post(registration_url, json={"agent_id": agent_id})
    if response.status_code == 200:
        print(response.json()["message"])

    while True:
        # Polling for commands (You need to implement the command-fetching mechanism here)
        time.sleep(5)
        # Send command response to master
        response_url = f"{master_url}/command_response/"
        command_output = "Sample command output"  # Replace with actual command execution logic
        response = requests.post(response_url, json={"agent_id": agent_id, "response": command_output})
        if response.status_code == 200:
            print(response.json()["message"])

if __name__ == "__main__":
    MASTER_URL = "http://127.0.0.1:8000"  # Replace with your master node URL
    agent(MASTER_URL)
