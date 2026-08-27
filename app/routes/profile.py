"""
User Profile routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User
from datetime import datetime

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@profile_bp.route('', methods=['GET'])
@login_required
def get_profile():
    """Get current user's profile."""
    return jsonify(current_user.to_dict()), 200

@profile_bp.route('', methods=['PUT'])
@login_required
def update_profile():
    """Update user's profile."""
    data = request.get_json()
    
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    if 'profile_picture' in data:
        current_user.profile_picture = data['profile_picture']
    
    if 'timezone' in data:
        current_user.timezone = data['timezone']
    
    if 'theme' in data:
        valid_themes = ['light', 'dark', 'system']
        if data['theme'] in valid_themes:
            current_user.theme = data['theme']
        else:
            return jsonify({'error': f'Invalid theme. Must be one of {valid_themes}'}), 400
    
    current_user.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@profile_bp.route('/preferences', methods=['GET'])
@login_required
def get_preferences():
    """Get user preferences."""
    return jsonify({
        'timezone': current_user.timezone,
        'theme': current_user.theme
    }), 200

@profile_bp.route('/preferences', methods=['PUT'])
@login_required
def update_preferences():
    """Update user preferences."""
    data = request.get_json()
    
    if 'timezone' in data:
        current_user.timezone = data['timezone']
    
    if 'theme' in data:
        valid_themes = ['light', 'dark', 'system']
        if data['theme'] in valid_themes:
            current_user.theme = data['theme']
        else:
            return jsonify({'error': f'Invalid theme. Must be one of {valid_themes}'}), 400
    
    current_user.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': {
                'timezone': current_user.timezone,
                'theme': current_user.theme
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update preferences'}), 500

@profile_bp.route('/account-settings', methods=['GET'])
@login_required
def get_account_settings():
    """Get account settings."""
    return jsonify({
        'email': current_user.email,
        'username': current_user.username,
        'full_name': current_user.full_name,
        'created_at': current_user.created_at.isoformat()
    }), 200

@profile_bp.route('/account-settings', methods=['PUT'])
@login_required
def update_account_settings():
    """Update account settings."""
    data = request.get_json()
    
    # Only allow updating full_name and email
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    # Email update would need verification, so we'll skip for now
    # if 'email' in data:
    #     # Check if email already exists
    #     existing = User.query.filter_by(email=data['email']).first()
    #     if existing and existing.id != current_user.id:
    #         return jsonify({'error': 'Email already in use'}), 409
    #     current_user.email = data['email']
    
    current_user.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Account settings updated successfully',
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update account settings'}), 500

@profile_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account."""
    data = request.get_json()
    
    # Verify password before deletion
    if not data or not data.get('password'):
        return jsonify({'error': 'Password is required to delete account'}), 400
    
    if not current_user.check_password(data['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    try:
        # Delete all user data (cascading)
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete account'}), 500
