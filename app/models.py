"""
Database models for HabitFlow application.
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    profile_picture = db.Column(db.String(255))
    timezone = db.Column(db.String(50), default='UTC')
    theme = db.Column(db.String(20), default='system')  # light, dark, system
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    habits = db.relationship('Habit', backref='user', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('HabitLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'profile_picture': self.profile_picture,
            'timezone': self.timezone,
            'theme': self.theme,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

class Category(db.Model):
    """Category model for organizing habits."""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # emoji or icon name
    color = db.Column(db.String(20))  # hex color
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    habits = db.relationship('Habit', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Habit(db.Model):
    """Habit model for tracking habits."""
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))  # emoji or custom icon URL
    color = db.Column(db.String(20))  # hex color
    
    # Habit type: boolean, count, duration, distance, numeric
    habit_type = db.Column(db.String(20), default='boolean', nullable=False)
    
    # Goal configuration
    goal_value = db.Column(db.Float)  # Target value
    goal_unit = db.Column(db.String(50))  # Unit (e.g., km, hours, glasses, pages)
    
    # Frequency: daily, weekly, monthly
    frequency = db.Column(db.String(20), default='daily', nullable=False)
    
    # Status: active, archived, disabled
    status = db.Column(db.String(20), default='active', nullable=False)
    
    is_favorite = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_logs=False):
        """Convert habit to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'habit_type': self.habit_type,
            'goal_value': self.goal_value,
            'goal_unit': self.goal_unit,
            'frequency': self.frequency,
            'status': self.status,
            'is_favorite': self.is_favorite,
            'display_order': self.display_order,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_logs:
            data['logs'] = [log.to_dict() for log in self.logs]
        return data

class HabitLog(db.Model):
    """Activity log for habits."""
    __tablename__ = 'habit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False, index=True)
    
    # Log values based on habit type
    value = db.Column(db.Float)  # For count, duration, distance, numeric types
    notes = db.Column(db.Text)
    
    # Timestamps
    logged_date = db.Column(db.Date, nullable=False, index=True)
    logged_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert log to dictionary."""
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'value': self.value,
            'notes': self.notes,
            'logged_date': self.logged_date.isoformat(),
            'logged_time': self.logged_time.isoformat() if self.logged_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
