# example_module.py
# Module describing a benign endpoint in the lab DVWA install.
MODULE = {
    "name": "login_form",
    "method": "POST",
    "url": "http://127.0.0.1:5000/login.php",
    "params": ["username", "password"],
}

def build_params(payload_variant):
    # payload_variant is a dict with keys for each parameter to send.
    # Use lab-controlled, benign values here.
    return {
        "username": payload_variant.get("username", "test_user"),
        "password": payload_variant.get("password", "test_pw"),
        "Login": "Login"
    }
