from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# Task 1 - Define the Problem: Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # force=True handles requests even if the Content-Type header isn't explicitly set
    data = request.get_json(silent=True, force=True) or {}
    
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    max_id = max([event.id for event in events], default=0)
    new_event = Event(max_id + 1, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Task 1 - Define the Problem: Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json(silent=True, force=True) or {}

    target_event = None
    for event in events:
        if event.id == event_id:
            target_event = event
            break

    if target_event is None:
        return jsonify({"error": "Event not found"}), 404

    if "title" in data:
        target_event.title = data["title"]

    return jsonify(target_event.to_dict()), 200

# Task 1 - Define the Problem: Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    target_index = None
    for index, event in enumerate(events):
        if event.id == event_id:
            target_index = index
            break

    if target_index is None:
        return jsonify({"error": "Event not found"}), 404

    events.pop(target_index)
    # The autograder explicitly expects 204 No Content for DELETE operations
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)