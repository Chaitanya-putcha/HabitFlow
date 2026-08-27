"""
Frontend views and page rendering.
"""
from flask import Blueprint, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
import os

views_bp = Blueprint('views', __name__)
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

@views_bp.route('/')
def index():
    """Landing page."""
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return send_from_directory(STATIC_DIR, 'index.html')

@views_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page."""
    return send_from_directory(STATIC_DIR, 'dashboard.html')

@views_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, filename)
