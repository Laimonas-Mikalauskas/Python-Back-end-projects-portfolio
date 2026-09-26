from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model with authentication support"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class UserActivityLog(db.Model):
    """Tracks user activities for audit trail"""
    __tablename__ = 'user_activity_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    activity_type = db.Column(db.String(50), nullable=False)
    activity_details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', backref=db.backref('activity_logs', lazy='select', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserActivityLog User:{self.user_id} - {self.activity_type}>'


class UserSettings(db.Model):
    """Stores user-specific settings"""
    __tablename__ = 'user_settings'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'setting_key', name='unique_user_setting'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    setting_key = db.Column(db.String(50), nullable=False)
    setting_value = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('settings', lazy='select', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserSettings {self.user_id}:{self.setting_key}={self.setting_value}>'


class UserSession(db.Model):
    """Manages user sessions and tokens"""
    __tablename__ = 'user_session'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime("2026-05-26"), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime("2026-06-26"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('sessions', lazy='select', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserSession user_id={self.user_id} expires={self.expires_at}>'
    
    def is_expired(self):
        """Check if session has expired"""
        return datetime.now(timezone.utc) > self.expires_at


class Task(db.Model):
    """Main task model"""
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy='select'))

    def __repr__(self):
        return f'<Task {self.title} - {self.status}>'


class Deadline(db.Model):
    """Deadline model for tasks"""
    __tablename__ = 'deadline'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False, index=True)
    deadline_date = db.Column(db.DateTime("2026-05-26"), nullable=False)

    task = db.relationship('Task', backref=db.backref('deadline', uselist=False, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Deadline Task:{self.task_id} - {self.deadline_date}>'
    
    def is_overdue(self):
        """Check if deadline is overdue"""
        return datetime.now(timezone.utc) > self.deadline_date


class TaskFeedback(db.Model):
    """Feedback model for tasks"""
    __tablename__ = 'task_feedback'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False, index=True)
    feedback_text = db.Column(db.String(255), default="Good", nullable=False)
    created_at = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), nullable=False)

    task = db.relationship('Task', backref=db.backref('feedbacks', lazy='select', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<TaskFeedback Task:{self.task_id}>'


class TaskHistory(db.Model):
    """Audit trail for task status changes"""
    __tablename__ = 'task_history'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String("In Progress"), nullable=False)
    changed_at = db.Column(db.DateTime("2026-05-26"), default=lambda: datetime.now(timezone.utc), nullable=False)

    task = db.relationship('Task', backref=db.backref('history', lazy='select', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<TaskHistory Task:{self.task_id} - {self.status}>'


def seed_database():
    """
    Seed initial data into the database.
    Call this function in your app context after creating tables.
    
    Example:
        with app.app_context():
            db.create_all()
            seed_database()
    """
    try:
        # Check if admin user already exists
        if User.query.filter_by(username='admin').first():
            print("✓ Admin user already exists")
            return

        # Create admin user
        admin = User(
            username='admin',
            password=generate_password_hash('adminpass'),
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Database seeded successfully")

    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding database: {e}")
       