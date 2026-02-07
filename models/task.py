from datetime import datetime
from extensions import db
import uuid


class Task(db.Model):
    """Task model for task management"""
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

    # Task details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='Other')
    tags = db.Column(db.JSON, default=list)

    # Task metrics
    priority = db.Column(db.Integer, default=3)  # 1-5, 1=highest
    impact = db.Column(db.Integer, default=5)  # 1-10
    complexity = db.Column(db.Integer, default=3)  # 1-5
    estimated_hours = db.Column(db.Float, default=1.0)

    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, completed, blocked, archived
    progress = db.Column(db.Integer, default=0)  # 0-100
    due_date = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime)

    # AI insights
    ai_insights = db.Column(db.JSON, default={
        'estimated_completion_time': None,
        'suggested_resources': [],
        'complexity_score': None,
        'recommended_approach': None
    })

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = db.Column(db.DateTime)

    # Indexes
    __table_args__ = (
        db.Index('idx_user_status', 'user_id', 'status'),
        db.Index('idx_user_priority', 'user_id', 'priority'),
        db.Index('idx_user_due_date', 'user_id', 'due_date'),
        db.Index('idx_user_category', 'user_id', 'category'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure due_date is datetime
        if 'due_date' in kwargs and isinstance(kwargs['due_date'], str):
            self.due_date = datetime.fromisoformat(kwargs['due_date'].replace('Z', '+00:00'))

    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'tags': self.tags,
            'priority': self.priority,
            'impact': self.impact,
            'complexity': self.complexity,
            'estimated_hours': self.estimated_hours,
            'status': self.status,
            'progress': self.progress,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ai_insights': self.ai_insights,
            'user_id': self.user_id,
            'is_overdue': self.is_overdue,
            'task_score': self.task_score,
            'days_until_due': self.days_until_due
        }

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.status == 'completed':
            return False
        return self.due_date and self.due_date < datetime.utcnow()

    @property
    def task_score(self):
        """Calculate task score based on priority and impact"""
        return (self.priority * 0.6) + (self.impact * 0.3) + (self.complexity * 0.1)

    @property
    def days_until_due(self):
        """Calculate days until due date"""
        if not self.due_date or self.status == 'completed':
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days

    def update_progress(self, progress):
        """Update task progress"""
        if not 0 <= progress <= 100:
            raise ValueError("Progress must be between 0 and 100")

        self.progress = progress
        if progress == 100 and self.status != 'completed':
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
            # Update user stats
            self.user.update_stats('task_completed', self.impact)

    def start_task(self):
        """Mark task as started"""
        if self.status == 'pending':
            self.status = 'in-progress'
            self.started_at = datetime.utcnow()

    def __repr__(self):
        return f'<Task {self.title}>'


class TaskHistory(db.Model):
    """Track task history for audit and analytics"""
    __tablename__ = 'task_history'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # created, updated, completed, deleted
    changes = db.Column(db.JSON)  # Store what changed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    task = db.relationship('Task', backref=db.backref('history', lazy=True))
    user = db.relationship('User', backref=db.backref('task_history', lazy=True))