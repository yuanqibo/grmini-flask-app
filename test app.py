from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyBcwY5RCaxhzr8jGm4bsLJe2BMdQJTjEEY")

@app.route("/")
def home():
    return "Gemini API 服务已启动！请使用 POST /ask 来访问。"
def ask_gemini():
    data = request.json
    prompt = data.get("prompt", "")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(port=5000)