# seed/seed_data.py - UPDATED VERSION
from app import create_app
from models.user import User
from models.task import Task
from extensions import db  # Changed from utils.database
from datetime import datetime, timedelta
import random
import uuid


def seed_database():
    """Seed the database with sample data"""
    app = create_app()  # Removed 'development' argument

    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create sample users
        users = []
        for i in range(3):
            user = User(
                email=f'user{i + 1}@example.com',
                username=f'user{i + 1}',
                name=f'User {i + 1}',
                password='password123',
                is_verified=True
            )
            users.append(user)
            db.session.add(user)

        db.session.commit()

        # Categories for tasks
        categories = ['Design', 'Engineering', 'Marketing', 'Finance', 'Research', 'Operations']

        # Task descriptions
        task_templates = [
            {
                'title': 'Redesign landing page',
                'description': 'Complete overhaul of the main landing page with new branding'
            },
            {
                'title': 'Optimize database queries',
                'description': 'Reduce query response time by 40%'
            },
            {
                'title': 'Launch email campaign',
                'description': 'Q1 product launch email sequence'
            },
            {
                'title': 'Set up CI/CD pipeline',
                'description': 'Automate testing and deployment workflow'
            },
            {
                'title': 'Budget review Q1',
                'description': 'Review and approve Q1 department budgets'
            },
            {
                'title': 'User research interviews',
                'description': 'Conduct 10 user interviews for feature validation'
            },
            {
                'title': 'Inventory system upgrade',
                'description': 'Migrate to new inventory management platform'
            },
            {
                'title': 'Design system documentation',
                'description': 'Document all design tokens and component specs'
            }
        ]

        # Create sample tasks for each user
        for user in users:
            for i in range(8):
                template = task_templates[i % len(task_templates)]
                due_date = datetime.utcnow() + timedelta(days=random.randint(1, 30))

                task = Task(
                    user_id=user.id,
                    title=f"{template['title']} - User {user.username}",
                    description=template['description'],
                    category=categories[i % len(categories)],
                    priority=random.randint(1, 5),
                    impact=random.randint(1, 10),
                    status=random.choice(['pending', 'in-progress', 'completed']),
                    progress=random.randint(0, 100),
                    due_date=due_date,
                    tags=['urgent', 'important'] if random.random() > 0.7 else [],
                    complexity=random.randint(1, 5),
                    estimated_hours=random.uniform(1, 20)
                )

                # If completed, set completed_at
                if task.status == 'completed':
                    task.completed_at = due_date - timedelta(days=random.randint(1, 5))

                db.session.add(task)

                # Update user stats
                if task.status == 'completed':
                    user.stats['completed_tasks'] = user.stats.get('completed_tasks', 0) + 1
                user.stats['total_tasks'] = user.stats.get('total_tasks', 0) + 1

        db.session.commit()

        print("✅ Database seeded successfully!")
        print(f"Created {len(users)} users and {len(users) * 8} tasks")


if __name__ == '__main__':
    seed_database()