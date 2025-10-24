MODULE = {"name":"search", "method":"GET", "url":"http://127.0.0.1:5000/search.php", "params":["q"]}
def build_params(payload_variant):
    return {"q": payload_variant.get("q","test")}
