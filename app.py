from flask import Flask, jsonify, render_template, request

from calculator import CalcError, safe_eval

app = Flask(__name__)


#@app.after_request
'''def set_security_headers(resp):
    """En-têtes de sécurité HTTP (vérifiés par le scan DAST)."""
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'; "
        "form-action 'self'; base-uri 'self'"
    )
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cache-Control"] = "no-store"
    return resp
'''

@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/api/evaluate")
def evaluate():
    data = request.get_json(silent=True) or {}
    expression = data.get("expression")
    angle = data.get("angle", "rad")
    if not isinstance(expression, str) or not expression.strip():
        return jsonify(error="Expression vide"), 400
    if angle not in ("deg", "rad"):
        return jsonify(error="Mode d'angle invalide"), 400
    try:
        return jsonify(result=safe_eval(expression, angle))
    except CalcError as exc:
        return jsonify(error=str(exc)), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
