"""
Habit routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Habit, Category
from datetime import datetime

habits_bp = Blueprint('habits', __name__, url_prefix='/api/habits')

@habits_bp.route('', methods=['GET'])
@login_required
def get_habits():
    """Get all habits for current user."""
    status = request.args.get('status', None)
    category_id = request.args.get('category_id', None)
    sort_by = request.args.get('sort_by', 'display_order')
    
    query = Habit.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Sorting options
    if sort_by == 'name':
        query = query.order_by(Habit.name)
    elif sort_by == 'created':
        query = query.order_by(Habit.created_at.desc())
    elif sort_by == 'updated':
        query = query.order_by(Habit.updated_at.desc())
    elif sort_by == 'favorite':
        query = query.order_by(Habit.is_favorite.desc(), Habit.display_order)
    else:
        query = query.order_by(Habit.display_order)
    
    habits = query.all()
    return jsonify([habit.to_dict() for habit in habits]), 200

@habits_bp.route('/<int:habit_id>', methods=['GET'])
@login_required
def get_habit(habit_id):
    """Get a specific habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    return jsonify(habit.to_dict(include_logs=True)), 200

@habits_bp.route('', methods=['POST'])
@login_required
def create_habit():
    """Create a new habit."""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Habit name is required'}), 400
    
    # Validate category if provided
    if data.get('category_id'):
        category = Category.query.filter_by(
            id=data['category_id'],
            user_id=current_user.id
        ).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
    
    habit = Habit(
        user_id=current_user.id,
        name=data['name'],
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        color=data.get('color', '#3b82f6'),
        habit_type=data.get('habit_type', 'boolean'),
        goal_value=data.get('goal_value'),
        goal_unit=data.get('goal_unit', ''),
        frequency=data.get('frequency', 'daily'),
        category_id=data.get('category_id')
    )
    
    try:
        db.session.add(habit)
        db.session.commit()
        return jsonify({
            'message': 'Habit created successfully',
            'habit': habit.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create habit'}), 500

@habits_bp.route('/<int:habit_id>', methods=['PUT'])
@login_required
def update_habit(habit_id):
    """Update a habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        habit.name = data['name']
    if 'description' in data:
        habit.description = data['description']
    if 'icon' in data:
        habit.icon = data['icon']
    if 'color' in data:
        habit.color = data['color']
    if 'habit_type' in data:
        habit.habit_type = data['habit_type']
    if 'goal_value' in data:
        habit.goal_value = data['goal_value']
    if 'goal_unit' in data:
        habit.goal_unit = data['goal_unit']
    if 'frequency' in data:
        habit.frequency = data['frequency']
    if 'status' in data:
        habit.status = data['status']
    if 'is_favorite' in data:
        habit.is_favorite = data['is_favorite']
    if 'display_order' in data:
        habit.display_order = data['display_order']
    if 'category_id' in data:
        habit.category_id = data['category_id']
    
    habit.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Habit updated successfully',
            'habit': habit.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update habit'}), 500

@habits_bp.route('/<int:habit_id>', methods=['DELETE'])
@login_required
def delete_habit(habit_id):
    """Delete a habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    try:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete habit'}), 500

@habits_bp.route('/<int:habit_id>/toggle-favorite', methods=['POST'])
@login_required
def toggle_favorite(habit_id):
    """Toggle habit favorite status."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    habit.is_favorite = not habit.is_favorite
    db.session.commit()
    
    return jsonify({
        'message': 'Favorite status updated',
        'habit': habit.to_dict()
    }), 200

@habits_bp.route('/<int:habit_id>/archive', methods=['POST'])
@login_required
def archive_habit(habit_id):
    """Archive a habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    habit.status = 'archived'
    db.session.commit()
    
    return jsonify({
        'message': 'Habit archived',
        'habit': habit.to_dict()
    }), 200

@habits_bp.route('/<int:habit_id>/restore', methods=['POST'])
@login_required
def restore_habit(habit_id):
    """Restore an archived habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    habit.status = 'active'
    db.session.commit()
    
    return jsonify({
        'message': 'Habit restored',
        'habit': habit.to_dict()
    }), 200
