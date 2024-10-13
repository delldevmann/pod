from flask import Flask, request, jsonify
import time

app = Flask(__name__)
agents = {}

@app.route('/register_agent', methods=['POST'])
def register_agent():
    agent_id = request.json.get('agent_id')
    if agent_id:
        agents[agent_id] = {
            "last_seen": time.ctime()
        }
        return jsonify({"message": f"Agent {agent_id} registered successfully."}), 200
    else:
        return jsonify({"error": "No agent_id provided"}), 400

@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify(agents), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
