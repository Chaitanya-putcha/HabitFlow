"""
Category routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Category, Habit
from datetime import datetime

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

# Default categories for new users
DEFAULT_CATEGORIES = [
    {'name': 'Health', 'icon': '❤️', 'color': '#ef4444'},
    {'name': 'Fitness', 'icon': '💪', 'color': '#f97316'},
    {'name': 'Learning', 'icon': '📚', 'color': '#8b5cf6'},
    {'name': 'Productivity', 'icon': '⚡', 'color': '#eab308'},
    {'name': 'Lifestyle', 'icon': '🌟', 'color': '#06b6d4'},
    {'name': 'Finance', 'icon': '💰', 'color': '#10b981'},
    {'name': 'Reading', 'icon': '📖', 'color': '#3b82f6'},
    {'name': 'Coding', 'icon': '💻', 'color': '#6b7280'},
]

@categories_bp.route('', methods=['GET'])
@login_required
def get_categories():
    """Get all categories for current user."""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify([cat.to_dict() for cat in categories]), 200

@categories_bp.route('/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    """Get a specific category."""
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    return jsonify(category.to_dict()), 200

@categories_bp.route('', methods=['POST'])
@login_required
def create_category():
    """Create a new category."""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400
    
    # Check if category name already exists for this user
    existing = Category.query.filter_by(
        user_id=current_user.id,
        name=data['name']
    ).first()
    
    if existing:
        return jsonify({'error': 'Category already exists'}), 409
    
    category = Category(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        color=data.get('color', '#3b82f6')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create category'}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    """Update a category."""
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    if 'icon' in data:
        category.icon = data['icon']
    if 'color' in data:
        category.color = data['color']
    
    category.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update category'}), 500

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Remove category from associated habits
    Habit.query.filter_by(category_id=category_id).update({'category_id': None})
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete category'}), 500

@categories_bp.route('/init-defaults', methods=['POST'])
@login_required
def initialize_default_categories():
    """Initialize default categories for new user."""
    # Check if user already has categories
    existing_count = Category.query.filter_by(user_id=current_user.id).count()
    
    if existing_count > 0:
        return jsonify({'error': 'User already has categories'}), 400
    
    try:
        for cat_data in DEFAULT_CATEGORIES:
            category = Category(
                user_id=current_user.id,
                name=cat_data['name'],
                icon=cat_data['icon'],
                color=cat_data['color'],
                is_default=True
            )
            db.session.add(category)
        
        db.session.commit()
        return jsonify({
            'message': 'Default categories initialized',
            'count': len(DEFAULT_CATEGORIES)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to initialize categories'}), 500
