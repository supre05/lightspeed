import requests


# Update profile
res = requests.post(f"http://127.0.0.1:5000/profile/2", json={
    "age": 28,
    "gender": "Female",
    "city": "Mumbai",
    "skills": ["acting", "dancing"],
    "genres": ["drama"],
    "languages": ["Hindi", "English"],
    "experience": 3
})
print("Profile Update:", res.json())

# Recommend profiles for job_id 1, hirer_id 1
res = requests.get(f"http://127.0.0.1:5000/recommend/profiles/1/1")
print("Profile Recommendations:", res.json())

# Recommend jobs for user_id 2
res = requests.get(f"http://127.0.0.1:5000/recommend/jobs/2")
print("Job Recommendations:", res.json())

# Recommend events for user_id 3 (Singer Lata)
res = requests.get(f"http://127.0.0.1:5000/recommend/events/5")
print("Event Recommendations for Cinematographer:", res.json())