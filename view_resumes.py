from extensions import db
from models import ResumeData
from app import app

with app.app_context():
    resumes = ResumeData.query.all()
    for resume in resumes:
        print(f"ID: {resume.id}")
        print(f"Registration ID: {resume.registration_id}")
        print(f"Name: {resume.name}")
        print(f"Age: {resume.age}")
        print(f"Gender: {resume.gender}")
        print(f"Location: {resume.location}")
        print(f"Skills: {resume.skills}")
        print(f"Languages: {resume.languages}")
        print(f"Experience: {resume.experience}")
        print(f"Awards: {resume.awards}")
        print(f"References: {resume.references}")
        print(f"Role: {resume.role}")
        print(f"Raw Text: {resume.text[:100]}...")  # print only first 100 chars
        print("-" * 60)
