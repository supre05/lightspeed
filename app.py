from flask import Flask,request,jsonify
from models import db, TalentProfile, db, User, TalentProfile, EventPost
from routes import recommendation_bp
from recommender import recommend_events_for_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommendation.db'  # or PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(recommendation_bp)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Recommendation System is running!"

@app.route('/profile/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    data = request.json
    profile = TalentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = TalentProfile(user_id=user_id)

    profile.age = data.get("age")
    profile.gender = data.get("gender")
    profile.city = data.get("city")
    profile.skills = ",".join(data.get("skills", []))
    profile.genres = ",".join(data.get("genres", []))
    profile.languages = ",".join(data.get("languages", []))
    profile.experience = data.get("experience")

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})
    

if __name__ == "__main__":
    app.run(debug=True)