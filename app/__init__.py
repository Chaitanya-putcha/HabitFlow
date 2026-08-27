"""
HabitFlow Application Package
"""
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='development'):
    """Application factory function."""
    app = Flask(__name__, static_folder=None)
    
    # Load configuration
    app.config.from_object(config[config_name])

    if config_name == 'production':
        if not app.config.get('SECRET_KEY') or app.config['SECRET_KEY'].startswith('dev-'):
            raise RuntimeError('SECRET_KEY must be set to a strong value in production')
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise RuntimeError('DATABASE_URL must be set in production')

    database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    if database_url and database_url.startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    @app.get('/health')
    def health_check():
        return jsonify(status='ok'), 200
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.views import views_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.habits import habits_bp
    from app.routes.categories import categories_bp
    from app.routes.logs import logs_bp
    from app.routes.statistics import statistics_bp
    from app.routes.profile import profile_bp
    from app.routes.calendar import calendar_bp
    
    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(calendar_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
