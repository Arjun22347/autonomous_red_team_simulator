# mock_target.py -- simple lab-only mock target with richer signals
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/login.php", methods=["GET","POST"])
def login():
    user = request.form.get("username", "")
    if "lab_user_1" in user:
        body = "<html><body>Welcome, lab_user_1! marker: A</body></html>"
        return make_response(body, 200)
    elif "lab_user_2" in user:
        body = "<html><body>Login failed. error: UNIQUE_ERROR_42</body></html>"
        return make_response(body, 200)
    elif "err500" in user or "err500_user" in user:
        # simulate server-side error with marker
        return make_response("Internal server error - ERR500_MARKER", 500)
    else:
        return make_response("<html><body>Regular response</body></html>", 200)

@app.route("/search.php", methods=["GET"])
def search():
    q = request.args.get("q","")
    if "needle" in q:
        return "<html><body>Found needle - marker: B</body></html>", 200
    return "<html><body>No results</body></html>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
