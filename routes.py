from flask import Blueprint, jsonify, request
from recommender import recommend_profiles_for_job, get_liked_profiles, boost_scores, recommend_jobs_for_user, recommend_events_for_user, combined_feed

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommend/profiles/<int:job_id>/<int:hirer_id>', methods=['GET'])
def recommend_profiles(job_id, hirer_id):
    ranked = recommend_profiles_for_job(job_id)
    liked_ids = get_liked_profiles(hirer_id)
    boosted = boost_scores(ranked, liked_ids)

    return jsonify([
        {"profile_id": pid, "score": round(score, 3)}
        for pid, score in boosted
    ])

@recommendation_bp.route('/recommend/jobs/<int:user_id>', methods=['GET'])
def recommend_jobs(user_id):
    ranked = recommend_jobs_for_user(user_id)
    return jsonify([
        {"job_id": jid, "score": round(score, 3)}
        for jid, score in ranked
    ])

@recommendation_bp.route('/recommend/events/<int:user_id>', methods=['GET'])
def recommend_events(user_id):
    matched_events = recommend_events_for_user(user_id)
    return jsonify([
        {"event_id": eid, "score": score}
        for eid, score in matched_events
    ])

@recommendation_bp.route('/recommend/feed/<int:user_id>', methods=['GET'])
def feed(user_id):
    items = combined_feed(user_id)
    return jsonify([
        {"type": t, "id": pid, "score": round(score, 2)}
        for t, pid, score in items
    ])

@recommendation_bp.route('/events', methods=['GET'])
def list_events():
    from models import EventPost
    events = EventPost.query.all()
    return jsonify([event.to_dict() for event in events])