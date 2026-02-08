from datetime import datetime, timezone
# from flask_bcrypt import generate_password_hash, check_password_hash
from extensions import db, bcrypt
import uuid


class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')
    preferences = db.Column(db.JSON, default={
        'theme': 'light',
        'notifications': True,
        'ai_enabled': True
    })
    stats = db.Column(db.JSON, default={
        'total_tasks': 0,
        'completed_tasks': 0,
        'avg_completion_time': 0,
        'productivity_score': 0
    })
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     if 'password' in kwargs:
    #         self.set_password(kwargs['password'])

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def update_stats(self, action, task_impact=None):
        """Update user statistics"""
        if action == 'task_completed':
            self.stats['completed_tasks'] = self.stats.get('completed_tasks', 0) + 1
            if task_impact:
                # Update average impact
                current_avg = self.stats.get('avg_impact', 0)
                completed = self.stats.get('completed_tasks', 1)
                self.stats['avg_impact'] = ((current_avg * (completed - 1)) + task_impact) / completed
        elif action == 'task_created':
            self.stats['total_tasks'] = self.stats.get('total_tasks', 0) + 1

        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'preferences': self.preferences,
            'stats': self.stats,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f'<User {self.email}>'


class UserPreferences(db.Model):
    """Separate table for user preferences"""
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True)
    theme = db.Column(db.String(20), default='light')
    notifications = db.Column(db.JSON, default={
        'email': True,
        'push': True,
        'task_reminders': True
    })
    ai_settings = db.Column(db.JSON, default={
        'enabled': True,
        'suggestions': True,
        'auto_categorize': False
    })
    display_settings = db.Column(db.JSON, default={
        'density': 'normal',
        'show_completed': True,
        'default_view': 'list'
    })

    user = db.relationship('User', backref=db.backref('preference', uselist=False))