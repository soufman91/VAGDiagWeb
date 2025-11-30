import json
import os
from flask import Flask, render_template, request

APP_TITLE = "VAGDiag Web – Décodeur codes VAG"

app = Flask(__name__)

def load_codes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "vag_codes.json")
    if not os.path.exists(json_path):
        return {}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

CODES = load_codes()

def normalize_code(raw: str) -> str:
    code = raw.strip().upper()
    if not code:
        return code
    if len(code) == 5 and code.startswith("P") and code[1:].isdigit():
        return code
    if code.isdigit():
        return code.lstrip("0") or "0"
    return code

def get_candidates(raw: str):
    code = normalize_code(raw)
    candidates = [code]
    if code.isdigit():
        candidates.append(code.zfill(5))
    candidates.append(raw.strip().upper())
    final = []
    seen = set()
    for c in candidates:
        if c not in seen:
            final.append(c)
            seen.add(c)
    return final

def search_code(raw: str):
    if not raw:
        return None, "Saisis un code avant de lancer la recherche."
    candidates = get_candidates(raw)
    for c in candidates:
        if c in CODES:
            return CODES[c], None
    return None, f"Code « {raw.upper()} » non trouvé dans la base. Ajoute-le dans vag_codes.json."

@app.route("/", methods=["GET", "POST"])
def index():
    code_input = ""
    result = None
    message = None
    if request.method == "POST":
        code_input = request.form.get("code", "").strip()
        result, message = search_code(code_input)
    return render_template("index.html", title=APP_TITLE, code_input=code_input, result=result, message=message)

if __name__ == "__main__":
    app.run(debug=True)
