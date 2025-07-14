import os
from flask import Flask, jsonify
from google.cloud import firestore

# Initialize Flask App
app = Flask(__name__)

# --- Configuration ---
# Your Google Cloud Project ID
GCP_PROJECT_ID = "ocean-beach-cafe"

# --- Firestore Connection ---
# The client will be initialized once when the app starts
db = firestore.Client(project=GCP_PROJECT_ID)


@app.route("/")
def hello_world():
    """Homepage route."""
    return "<h1>Welcome to the Restaurant Scheduler!</h1>"


@app.route("/employees")
def get_employees():
    """API route to fetch and display all employees from Firestore."""
    try:
        employees_ref = db.collection("employees")
        docs = employees_ref.stream()

        # Convert the documents to a list of dictionaries
        employee_list = []
        for doc in docs:
            employee_data = doc.to_dict()
            employee_data['id'] = doc.id  # Add the document ID
            employee_list.append(employee_data)

        # Return the list as a JSON response
        return jsonify(employee_list)

    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # The app will run on port 8080 by default
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
