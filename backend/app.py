from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ai_service import generate_ai_reply
import os

app = Flask(__name__)
CORS(app)  # Cho phép frontend gọi API từ domain khác (VD: file:// hoặc localhost)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt.strip():
        return jsonify({"reply": "Vui lòng nhập nội dung để tôi có thể trả lời."})
    
    reply = generate_ai_reply(prompt, context_file=None)
    return jsonify({"reply": reply})

@app.route("/")
def home():
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
    return send_from_directory(frontend_path, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
    return send_from_directory(frontend_path, path)

if __name__ == "__main__":
    app.run(debug=True)
