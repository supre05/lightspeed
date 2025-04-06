from models import db, User, TalentProfile, JobPost, Interaction, EventPost
from app import app
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Job Hirers
    hirer1 = User(name="Director Raj", role="job_hirer")
    hirer2 = User(name="Music Director Anu", role="job_hirer")

    # Create Job Seekers
    seeker1 = User(name="Actor Aisha", role="job_seeker")
    seeker2 = User(name="Actor Rahul", role="job_seeker")
    seeker3 = User(name="Singer Lata", role="job_seeker")
    seeker4 = User(name="Dancer Arjun", role="job_seeker")
    seeker5 = User(name="Cinematographer Ravi", role="job_seeker")

    db.session.add_all([hirer1, hirer2, seeker1, seeker2, seeker3, seeker4, seeker5])
    db.session.flush()  # Get IDs for foreign keys

    # Create Talent Profiles
    p1 = TalentProfile(user_id=seeker1.id, age=25, gender="Female", city="Mumbai", skills="acting,dancing", genres="drama", experience=3, languages="Hindi,English")
    p2 = TalentProfile(user_id=seeker2.id, age=30, gender="Male", city="Delhi", skills="acting,comedy", genres="comedy", experience=5, languages="Hindi")
    p3 = TalentProfile(user_id=seeker3.id, age=27, gender="Female", city="Mumbai", skills="singing", genres="classical", experience=4, languages="Hindi,Tamil")
    p4 = TalentProfile(user_id=seeker4.id, age=22, gender="Male", city="Bangalore", skills="dancing", genres="contemporary", experience=2, languages="Kannada")
    p5 = TalentProfile(user_id=seeker5.id, age=35, gender="Male", city="Hyderabad", skills="cinematography", genres="action", experience=10, languages="Telugu")

    db.session.add_all([p1, p2, p3, p4, p5])

    # Create Job Posts
    j1 = JobPost(hirer_id=hirer1.id, role="actor", required_age_min=20, required_age_max=30, gender="Female", city="Mumbai", skills_required="acting", genres="drama", experience_required=2)
    j2 = JobPost(hirer_id=hirer2.id, role="singer", required_age_min=25, required_age_max=35, gender="Female", city="Mumbai", skills_required="singing", genres="classical", experience_required=3)

    db.session.add_all([j1, j2])

    # Add some interactions
    i1 = Interaction(user_id=hirer1.id, content_type="talent_profile", content_id=p1.id, interaction_type="liked")
    i2 = Interaction(user_id=hirer1.id, content_type="talent_profile", content_id=p2.id, interaction_type="liked")
    i3 = Interaction(user_id=hirer2.id, content_type="talent_profile", content_id=p3.id, interaction_type="liked")

    db.session.add_all([i1, i2, i3])


    # Sample event posts
    event1 = EventPost(
        hirer_id=1,
        title="Carnatic Vocal Concert",
        description="An evening of traditional Carnatic music.",
        city="Chennai",
        date=date(2025, 4, 15)
    )

    event2 = EventPost(
        hirer_id=2,
        title="Stand up comedy Performance",
        description="Stand up comedy by Nirmal Pillai.",
        city="Bangalore",
        date=date(2025, 4, 20)
    )

    db.session.add_all([event1, event2])
    db.session.commit()