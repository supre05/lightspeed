from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)

# ------------------- VIRTUAL TALENT MANAGER (AI CHAT) -------------------
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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")
    response = chatbot(user_input)
    return jsonify({"response": response})

# ------------------- RESUME MATCHER -------------------

def load_profiles():
    with open("data/profiles.json") as f:
        return json.load(f)

def profile_to_text(profile):
    return " ".join([
        profile["profession"],
        str(profile["experience_years"]),
        " ".join(profile["skills"]),
        " ".join(profile["awards"]),
        profile["availability"],
        profile["location"],
        profile["job_type"],
        " ".join(profile["languages"]),
        " ".join(profile["tools"])
    ])

@app.route("/match", methods=["POST"])
def match():
    data = request.json
    job_description = data.get("job_description", "")
    profiles = load_profiles()
    texts = [profile_to_text(p) for p in profiles]
    texts.append(job_description)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    cos_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

    for i, score in enumerate(cos_sim):
        profiles[i]["match_score"] = round(float(score), 4)

    sorted_profiles = sorted(profiles, key=lambda x: x["match_score"], reverse=True)
    return jsonify(sorted_profiles)

# ------------------- SIGNUP FLOW -------------------

@app.route("/")
def home():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    user_type = request.form.get("userType")

    # You can save the form data here if needed

    if user_type == "individual":
        return redirect(url_for("talent_manager"))
    else:
        return redirect(url_for("resume_matcher"))

@app.route("/talent-manager")
def talent_manager():
    return render_template("talent_manager.html")

@app.route("/resume-matcher")
def resume_matcher():
    return render_template("index2.html")

# ------------------- MAIN -------------------

if __name__ == "__main__":
    app.run(debug=True)

