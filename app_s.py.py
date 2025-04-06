from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    user_type = request.form.get("userType")

    # Handle file uploads (optional)
    if user_type == "individual":
        cv_file = request.files.get("cv")
        if cv_file:
            cv_file.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_file.filename))
        # Could store user info in a database or session here
        return redirect(url_for("talent_agent"))
    elif user_type == "organization":
        bio_file = request.files.get("bio")
        if bio_file:
            bio_file.save(os.path.join(app.config["UPLOAD_FOLDER"], bio_file.filename))
        return redirect(url_for("resume_matcher"))

@app.route("/talent-agent")
def talent_agent():
    return render_template("talent_agent.html")

@app.route("/resume-matcher")
def resume_matcher():
    return render_template("index.html")  # From original ResumeMatcher

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    response = chatbot(user_input)
    return jsonify({"response": response})


# Virtual Agent Logic
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access the variable
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 250}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result[0]['generated_text'].split("### Response:")[-1].strip() if isinstance(result, list) else result

def chatbot(user_input):
    if "email" in user_input.lower() or "draft" in user_input.lower():
        prompt = f"""### Instruction:
You're a virtual talent agent. Draft a professional email on behalf of your client: {user_input}
### Response:"""
    elif "contract" in user_input.lower() or "legal" in user_input.lower():
        prompt = f"""### Instruction:
You're a virtual talent agent. Provide a general legal overview or contract clause recommendations for this request: {user_input}
### Response:"""
    elif "schedule" in user_input.lower():
        prompt = f"""### Instruction:
You're a talent agent managing a calendar. Assist in scheduling this: {user_input}
### Response:"""
    elif "resume tips" in user_input.lower():
        profession = user_input.split("for")[-1].strip()
        prompt = f"""### Instruction:
You're a virtual agent. Give smart, current resume tips for a {profession} in the entertainment industry.
### Response:"""
    elif "what is" in user_input.lower() or "explain" in user_input.lower():
        topic = user_input.split("about")[-1].strip()
        prompt = f"""### Instruction:
You're a talent agent. Explain the following industry term in beginner-friendly terms: {topic}
### Response:"""
    else:
        prompt = f"""### Instruction:
You're a helpful and professional virtual agent. Help the client with this request: {user_input}
### Response:"""

    return query_model(prompt)


if __name__ == '__main__':
    app.run(debug=True)
