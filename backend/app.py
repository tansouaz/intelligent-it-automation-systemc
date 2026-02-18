from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# Temporary in-memory storage (later we move to DB)
tickets = []

@app.route("/")
def home():
    return jsonify({"message": "Intelligent IT Automation Backend Running"})


@app.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    ticket = {
        "id": len(tickets) + 1,
        "title": data.get("title"),
        "description": data.get("description"),
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending",
        "priority": "not_analyzed"
    }

    tickets.append(ticket)

    # 🔥 Send ticket to n8n webhook
    try:
        requests.post(
            "http://localhost:5678/webhook/ticket-created",
            json=ticket,
            timeout=3
        )
        print("Sent to n8n successfully")
    except Exception as e:
        print("n8n webhook failed:", e)

    return jsonify(ticket), 201


@app.route("/tickets", methods=["GET"])
def get_tickets():
    return jsonify(tickets)


if __name__ == "__main__":
    app.run(debug=True)
