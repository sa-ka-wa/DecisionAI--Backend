# reset_db.py
from app import create_app, db

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("✅ Dropped all tables")

    # Create fresh tables
    db.create_all()
    print("✅ Created fresh tables")

    # Optional: Seed with test data
    from seed.seed_data import seed_database

    seed_database()
    print("✅ Seeded with test data")
