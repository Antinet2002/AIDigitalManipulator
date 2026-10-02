from flask import Flask, render_template, request, jsonify
from analyzer import analyze_text

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please enter a message to analyze."}), 400

    return jsonify(analyze_text(text))

if __name__ == "__main__":
    app.run(debug=True)
