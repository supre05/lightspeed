# parser.py
import fitz  # PyMuPDF
import uuid
import requests
import json
import re
from models import ResumeData
from extensions import db
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access the variable
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join(page.get_text() for page in doc)

def generate_registration_id():
    return f"ENT-{uuid.uuid4().hex[:8].upper()}"

def format_prompt(text):
    return f"""
You are an assistant that extracts structured data from resumes in the entertainment industry.

Given the following resume text, return a JSON object with the following fields:
- Name
- Age
- Gender
- Locations
- Skills
- Languages
- Experience
- Awards
- References
- Role

If any fields are missing, return "Not found" for those.

Resume:
{text}
"""

def query_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.3, "max_new_tokens": 512}
    }
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        elif isinstance(output, dict) and "generated_text" in output:
            return output["generated_text"]
        else:
            return str(output)
    else:
        raise Exception(f"Hugging Face API error: {response.status_code}\n{response.text}")

def safe_json_field(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value if value is not None else "Not found"

def parse_resume(pdf_path, session):
    resume_text = extract_text_from_pdf(pdf_path)
    prompt = format_prompt(resume_text)
    raw_output = query_huggingface(prompt)

    print("\n[RAW OUTPUT FROM HF MODEL]:\n", raw_output)

    try:
        json_match = re.search(r'({.*})', raw_output, re.DOTALL)
        if json_match:
            parsed_data = json.loads(json_match.group(1))
        else:
            parsed_data = {"Raw Output": raw_output}
    except json.JSONDecodeError:
        parsed_data = {"Raw Output": raw_output}

    resume = ResumeData(
        registration_id=generate_registration_id(),
        name=safe_json_field(parsed_data.get("Name", "Not found")),
        age=safe_json_field(parsed_data.get("Age", "Not found")),
        gender=safe_json_field(parsed_data.get("Gender", "Not found")),
        location=safe_json_field(parsed_data.get("Locations", "Not found")),
        skills=safe_json_field(parsed_data.get("Skills", "Not found")),
        languages=safe_json_field(parsed_data.get("Languages", "Not found")),
        experience=safe_json_field(parsed_data.get("Experience", "Not found")),
        awards=safe_json_field(parsed_data.get("Awards", "Not found")),
        references=safe_json_field(parsed_data.get("References", "Not found")),
        role=safe_json_field(parsed_data.get("Role", "Not found")),
        text=resume_text
    )

    session.add(resume)
    session.commit()
    return resume

if __name__ == "__main__":
    import sys
    from sqlalchemy.orm import sessionmaker
    from extensions import db
    from app import app

    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        sample_pdf_path = "Sudiksha Profile_WiSH.pdf"
        result = parse_resume(sample_pdf_path, session)

        print("\n✅ Parsed Resume Saved to DB:")
        print(result.__dict__)
