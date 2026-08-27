"""
Habit Log routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import HabitLog, Habit
from datetime import datetime, date

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@logs_bp.route('', methods=['GET'])
@login_required
def get_logs():
    """Get habit logs with optional filters."""
    habit_id = request.args.get('habit_id', None)
    date_from = request.args.get('date_from', None)
    date_to = request.args.get('date_to', None)
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = HabitLog.query.filter_by(user_id=current_user.id)
    
    if habit_id:
        query = query.filter_by(habit_id=habit_id)
    
    if date_from:
        try:
            from_date = datetime.fromisoformat(date_from).date()
            query = query.filter(HabitLog.logged_date >= from_date)
        except ValueError:
            return jsonify({'error': 'Invalid date_from format'}), 400
    
    if date_to:
        try:
            to_date = datetime.fromisoformat(date_to).date()
            query = query.filter(HabitLog.logged_date <= to_date)
        except ValueError:
            return jsonify({'error': 'Invalid date_to format'}), 400
    
    # Sort by date descending (most recent first)
    logs = query.order_by(HabitLog.logged_date.desc()).limit(limit).offset(offset).all()
    
    return jsonify([log.to_dict() for log in logs]), 200

@logs_bp.route('/<int:log_id>', methods=['GET'])
@login_required
def get_log(log_id):
    """Get a specific log."""
    log = HabitLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    
    if not log:
        return jsonify({'error': 'Log not found'}), 404
    
    return jsonify(log.to_dict()), 200

@logs_bp.route('', methods=['POST'])
@login_required
def create_log():
    """Create a new activity log."""
    data = request.get_json()
    
    if not data or not data.get('habit_id'):
        return jsonify({'error': 'Habit ID is required'}), 400
    
    # Verify habit belongs to current user
    habit = Habit.query.filter_by(id=data['habit_id'], user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    # Parse logged date
    try:
        if data.get('logged_date'):
            logged_date = datetime.fromisoformat(data['logged_date']).date()
        else:
            logged_date = date.today()
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid logged_date format'}), 400
    
    # Parse logged time if provided
    logged_time = None
    if data.get('logged_time'):
        try:
            logged_time = datetime.fromisoformat(data['logged_time']).time()
        except ValueError:
            return jsonify({'error': 'Invalid logged_time format'}), 400
    
    log = HabitLog(
        user_id=current_user.id,
        habit_id=data['habit_id'],
        value=data.get('value'),  # For non-boolean types
        notes=data.get('notes', ''),
        logged_date=logged_date,
        logged_time=logged_time
    )
    
    try:
        db.session.add(log)
        db.session.commit()
        return jsonify({
            'message': 'Activity logged successfully',
            'log': log.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create log'}), 500

@logs_bp.route('/<int:log_id>', methods=['PUT'])
@login_required
def update_log(log_id):
    """Update a log."""
    log = HabitLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    
    if not log:
        return jsonify({'error': 'Log not found'}), 404
    
    data = request.get_json()
    
    if 'value' in data:
        log.value = data['value']
    if 'notes' in data:
        log.notes = data['notes']
    if 'logged_date' in data:
        try:
            log.logged_date = datetime.fromisoformat(data['logged_date']).date()
        except ValueError:
            return jsonify({'error': 'Invalid logged_date format'}), 400
    if 'logged_time' in data and data['logged_time']:
        try:
            log.logged_time = datetime.fromisoformat(data['logged_time']).time()
        except ValueError:
            return jsonify({'error': 'Invalid logged_time format'}), 400
    
    log.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Log updated successfully',
            'log': log.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update log'}), 500

@logs_bp.route('/<int:log_id>', methods=['DELETE'])
@login_required
def delete_log(log_id):
    """Delete a log."""
    log = HabitLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    
    if not log:
        return jsonify({'error': 'Log not found'}), 404
    
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({'message': 'Log deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete log'}), 500

@logs_bp.route('/habit/<int:habit_id>/date/<string:log_date>', methods=['GET'])
@login_required
def get_logs_by_date(habit_id, log_date):
    """Get all logs for a habit on a specific date."""
    # Verify habit belongs to current user
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    try:
        target_date = datetime.fromisoformat(log_date).date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    logs = HabitLog.query.filter_by(
        habit_id=habit_id,
        logged_date=target_date
    ).order_by(HabitLog.logged_time.desc()).all()
    
    return jsonify([log.to_dict() for log in logs]), 200
