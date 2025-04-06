from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)  # job_seeker or job_hirer

class TalentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    city = db.Column(db.String)
    skills = db.Column(db.String)  # comma-separated
    genres = db.Column(db.String) # not required
    experience = db.Column(db.Float)
    languages = db.Column(db.String)

class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hirer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String)
    required_age_min = db.Column(db.Integer)
    required_age_max = db.Column(db.Integer)
    gender = db.Column(db.String)
    city = db.Column(db.String)
    skills_required = db.Column(db.String)
    genres = db.Column(db.String)
    experience_required = db.Column(db.Float)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content_type = db.Column(db.String)  # 'job_post' or 'talent_profile'
    content_id = db.Column(db.Integer)
    interaction_type = db.Column(db.String)  # liked, viewed, applied, hired


class EventPost(db.Model):
    _tablename_ = 'event_posts'
    id = db.Column(db.Integer, primary_key=True)
    hirer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hirer = db.relationship("User", backref="events")

    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    city = db.Column(db.String(50))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "hirer_id": self.hirer_id,
            "title": self.title,
            "description": self.description,
            "city": self.city,
            "date": self.date.isoformat() if self.date else None
        }