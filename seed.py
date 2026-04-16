from app import create_app, db
from app.models import User, Mood
from flask_bcrypt import Bcrypt
from faker import Faker
import random

fake = Faker()
bcrypt = Bcrypt()

app = create_app()

with app.app_context():

    print("Seeding database...")

  
    db.drop_all()
    db.create_all()

#1. create users
    users = []

    for _ in range(50):
        user = User(
            username=fake.user_name(),
            password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # #2. create moods
    mood_options = [
    "happy", "sad", "excited",
    "tired", "angry", "calm",
    "anxious", "motivated",
    "bored", "grateful"
]

    note_templates = [
        "Feeling really {mood} today after everything that happened.",
        "Had a {mood} morning, trying to stay positive.",
        "Not sure why but I’ve been feeling {mood} lately.",
        "Today was a very {mood} day at work.",
        "I woke up feeling {mood} and it carried through the day.",
        "Honestly feeling quite {mood}, but I’m managing.",
        "It’s been a {mood} kind of day overall.",
        "Feeling {mood} after talking to a friend.",
        "Work today made me feel {mood}.",
        "Just one of those {mood} days — nothing more to say."
    ]
    moods = []

    for user in users:
        for _ in range(5):  # 5 moods per user
            mood = random.choice(mood_options)

            note = random.choice(note_templates).format(mood=mood)

            moods.append(
                Mood(
                    mood=mood,
                    note=note,
                    user_id=user.id
                )
            )

    db.session.add_all(moods)
    db.session.commit()

    print("Seeding complete!")