import requests
import time

# Agent ID for this specific agent
agent_id = "agent-001"  # Each agent should have a unique ID

# Flask server URL
flask_url = "http://localhost:5000"  # Update with the public URL of your Flask server

# Register agent with the master
def register_agent():
    try:
        response = requests.post(f"{flask_url}/register_agent", json={"agent_id": agent_id})
        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(f"Failed to register. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to master node: {e}")

if __name__ == "__main__":
    while True:
        register_agent()
        time.sleep(10)  # Poll every 10 seconds to simulate agent activity
