import math
import subprocess  # noqa

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
SECRET_KEY = "admin123"  # secret en dur (mauvaise pratique)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


# VULNERABILITE 1 : eval() sur une entrée utilisateur => exécution de code arbitraire
@app.post("/api/evaluate")
def evaluate():
    data = request.get_json(silent=True) or {}
    expression = str(data.get("expression", "")).replace("^", "**")
    try:
        result = eval(expression, {"sqrt": math.sqrt, "pi": math.pi})
        return jsonify(result=result)
    except Exception as exc:
        return jsonify(error=str(exc)), 400


# VULNERABILITE 2 : route non authentifiée + injection de commande
@app.get("/admin/run")
def run_cmd():
    cmd = request.args.get("cmd", "echo hello")
    return subprocess.check_output(cmd, shell=True)


# VULNERABILITE 3 : pas d'en-têtes de sécurité (CSP, X-Frame-Options...) => alertes ZAP

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug en prod = dangereux
