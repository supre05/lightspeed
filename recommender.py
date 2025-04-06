import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import User, TalentProfile, JobPost, Interaction, EventPost, db
from sentence_transformers import SentenceTransformer, util
from models import TalentProfile, EventPost
def get_profiles():
    return TalentProfile.query.all()

def get_job_post(job_id):
    return JobPost.query.filter_by(id=job_id).first()

def recommend_profiles_for_job(job_id):
    job = get_job_post(job_id)
    profiles = get_profiles()

    profile_data = []
    ids = []

    for profile in profiles:
        combined_features = f"{profile.gender} {profile.city} {profile.skills} {profile.genres} {profile.languages}"
        profile_data.append(combined_features)
        ids.append(profile.id)

    job_features = f"{job.gender} {job.city} {job.skills_required} {job.genres}"

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_features] + profile_data)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    ranked = sorted(zip(ids, similarities), key=lambda x: x[1], reverse=True)
    return ranked[:10]  # top 10 matches

def get_liked_profiles(user_id):
    interactions = Interaction.query.filter_by(user_id=user_id, interaction_type='liked', content_type='talent_profile').all()
    return set(i.content_id for i in interactions)

def boost_scores(ranked, liked_ids):
    boosted = []
    for pid, score in ranked:
        if pid in liked_ids:
            score *= 1.5  # Boost liked ones
        boosted.append((pid, score))
    return sorted(boosted, key=lambda x: x[1], reverse=True)

def recommend_jobs_for_user(user_id):
    profile = TalentProfile.query.filter_by(user_id=user_id).first()
    jobs = JobPost.query.all()

    job_data = []
    ids = []

    for job in jobs:
        combined = f"{job.gender} {job.city} {job.skills_required} {job.genres}"
        job_data.append(combined)
        ids.append(job.id)

    seeker_features = f"{profile.gender} {profile.city} {profile.skills} {profile.genres}"

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([seeker_features] + job_data)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    ranked = sorted(zip(ids, similarities), key=lambda x: x[1], reverse=True)
    return ranked[:10]

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_events_for_user(user_id, threshold=0.3):
    from models import TalentProfile, EventPost

    profile = TalentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return []

    # Combine relevant fields into one text blob
    user_text = f"{profile.skills or ''} {profile.genres or ''} {profile.languages or ''}"
    user_embedding = model.encode(user_text, convert_to_tensor=True)

    events = EventPost.query.all()
    matched_events = []

    for event in events:
        event_text = f"{event.title or ''} {event.description or ''} {event.city or ''}"
        event_embedding = model.encode(event_text, convert_to_tensor=True)

        similarity = util.cos_sim(user_embedding, event_embedding).item()

        if similarity >= threshold:
            matched_events.append((event.id, round(similarity, 3)))

    return matched_events



def combined_feed(user_id):
    jobs = recommend_jobs_for_user(user_id)
    events = recommend_events_for_user(user_id)

    feed_items = [("job", jid, score) for jid, score in jobs] + \
                 [("event", eid, score) for eid, score in events]

    return sorted(feed_items, key=lambda x: x[2], reverse=True)