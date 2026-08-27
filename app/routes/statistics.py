"""
Statistics and Analytics routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Habit, HabitLog
from datetime import datetime, date, timedelta
from sqlalchemy import func

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/overview', methods=['GET'])
@login_required
def get_statistics_overview():
    """Get overall statistics."""
    today = date.today()
    
    # Get time period
    days = request.args.get('days', 30, type=int)
    start_date = today - timedelta(days=days)
    
    # Total logs
    total_logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= start_date
    ).count()
    
    # Logs by day average
    avg_logs_per_day = total_logs / days if days > 0 else 0
    
    # Get all habits
    all_habits = Habit.query.filter_by(user_id=current_user.id).all()
    
    # Completion stats
    completed_habits = 0
    partially_completed = 0
    not_completed = 0
    
    for habit in all_habits:
        logs_count = HabitLog.query.filter_by(habit_id=habit.id).filter(
            HabitLog.logged_date >= start_date
        ).count()
        
        if habit.goal_value:
            if logs_count >= habit.goal_value:
                completed_habits += 1
            elif logs_count > 0:
                partially_completed += 1
            else:
                not_completed += 1
        else:
            if logs_count > 0:
                completed_habits += 1
            else:
                not_completed += 1
    
    return jsonify({
        'period_days': days,
        'total_logs': total_logs,
        'avg_logs_per_day': round(avg_logs_per_day, 2),
        'completed_habits': completed_habits,
        'partially_completed': partially_completed,
        'not_completed': not_completed,
        'completion_rate': round((completed_habits / len(all_habits) * 100) if all_habits else 0, 2)
    }), 200

@statistics_bp.route('/habit/<int:habit_id>', methods=['GET'])
@login_required
def get_habit_statistics(habit_id):
    """Get statistics for a specific habit."""
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()
    
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    
    today = date.today()
    days = request.args.get('days', 90, type=int)
    start_date = today - timedelta(days=days)
    
    # Get all logs for this habit
    logs = HabitLog.query.filter_by(habit_id=habit_id).filter(
        HabitLog.logged_date >= start_date
    ).all()
    
    # Calculate statistics
    total_logs = len(logs)
    total_value = sum(log.value or 0 for log in logs)
    avg_value = total_value / total_logs if total_logs > 0 else 0
    max_value = max((log.value for log in logs if log.value), default=0)
    min_value = min((log.value for log in logs if log.value), default=0)
    
    # Completion percentage
    completion_percentage = (total_logs / days * 100) if days > 0 else 0
    
    # Logs by day of week
    logs_by_day = {}
    for i in range(7):
        logs_by_day[i] = 0
    
    for log in logs:
        day_of_week = log.logged_date.weekday()
        logs_by_day[day_of_week] += 1
    
    # Logs by week (last 12 weeks)
    logs_by_week = {}
    for i in range(12):
        week_start = today - timedelta(weeks=12-i)
        week_end = week_start + timedelta(days=6)
        week_logs = [log for log in logs if week_start <= log.logged_date <= week_end]
        logs_by_week[f"Week {i+1}"] = len(week_logs)
    
    return jsonify({
        'habit_id': habit_id,
        'habit_name': habit.name,
        'period_days': days,
        'total_logs': total_logs,
        'total_value': round(total_value, 2),
        'average_value': round(avg_value, 2),
        'max_value': max_value,
        'min_value': min_value,
        'completion_percentage': round(completion_percentage, 2),
        'logs_by_day_of_week': logs_by_day,
        'logs_by_week': logs_by_week
    }), 200

@statistics_bp.route('/monthly', methods=['GET'])
@login_required
def get_monthly_statistics():
    """Get monthly statistics."""
    month = request.args.get('month', None)
    year = request.args.get('year', None)
    
    today = date.today()
    
    if month and year:
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return jsonify({'error': 'Invalid month or year'}), 400
    else:
        month = today.month
        year = today.year
    
    # Get first and last day of month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Get logs for this month
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= first_day,
        HabitLog.logged_date <= last_day
    ).all()
    
    # Logs by day
    logs_by_day = {}
    for day in range(1, (last_day - first_day).days + 2):
        current_date = first_day + timedelta(days=day-1)
        date_key = current_date.isoformat()
        day_logs = [log for log in logs if log.logged_date == current_date]
        logs_by_day[date_key] = len(day_logs)
    
    return jsonify({
        'month': month,
        'year': year,
        'total_logs': len(logs),
        'logs_by_day': logs_by_day
    }), 200

@statistics_bp.route('/yearly', methods=['GET'])
@login_required
def get_yearly_statistics():
    """Get yearly statistics."""
    year = request.args.get('year', date.today().year, type=int)
    
    # Get all logs for this year
    first_day = date(year, 1, 1)
    last_day = date(year, 12, 31)
    
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= first_day,
        HabitLog.logged_date <= last_day
    ).all()
    
    # Logs by month
    logs_by_month = {}
    for month in range(1, 13):
        month_key = f"{year}-{month:02d}"
        month_logs = [log for log in logs if log.logged_date.month == month]
        logs_by_month[month_key] = len(month_logs)
    
    return jsonify({
        'year': year,
        'total_logs': len(logs),
        'logs_by_month': logs_by_month
    }), 200

@statistics_bp.route('/top-habits', methods=['GET'])
@login_required
def get_top_habits():
    """Get top habits by activity."""
    limit = request.args.get('limit', 10, type=int)
    days = request.args.get('days', 30, type=int)
    
    today = date.today()
    start_date = today - timedelta(days=days)
    
    # Get habit log counts
    habit_counts = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= start_date
    ).with_entities(HabitLog.habit_id, func.count(HabitLog.id)).group_by(
        HabitLog.habit_id
    ).order_by(func.count(HabitLog.id).desc()).limit(limit).all()
    
    top_habits = []
    for habit_id, count in habit_counts:
        habit = Habit.query.get(habit_id)
        if habit:
            top_habits.append({
                'habit': habit.to_dict(),
                'logs_count': count
            })
    
    return jsonify({
        'period_days': days,
        'top_habits': top_habits
    }), 200

@statistics_bp.route('/streak-data', methods=['GET'])
@login_required
def get_streak_data():
    """Get streak information for all habits."""
    all_habits = Habit.query.filter_by(user_id=current_user.id).all()
    
    streak_data = []
    for habit in all_habits:
        current_streak = calculate_current_streak(habit)
        longest_streak = calculate_longest_streak(habit)
        
        streak_data.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'habit_type': habit.habit_type,
            'current_streak': current_streak,
            'longest_streak': longest_streak
        })
    
    # Sort by current streak
    streak_data.sort(key=lambda x: x['current_streak'], reverse=True)
    
    return jsonify({
        'total_habits': len(all_habits),
        'streaks': streak_data
    }), 200

def calculate_current_streak(habit):
    """Calculate current streak for a habit."""
    today = date.today()
    logs = HabitLog.query.filter_by(habit_id=habit.id).order_by(
        HabitLog.logged_date.desc()
    ).all()
    
    if not logs:
        return 0
    
    streak = 0
    current_date = today
    
    if habit.frequency == 'daily':
        for log in logs:
            if log.logged_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif log.logged_date < current_date:
                break
    
    return streak

def calculate_longest_streak(habit):
    """Calculate longest streak for a habit."""
    logs = HabitLog.query.filter_by(habit_id=habit.id).order_by(
        HabitLog.logged_date.asc()
    ).all()
    
    if not logs:
        return 0
    
    max_streak = 0
    current_streak = 0
    current_date = None
    
    if habit.frequency == 'daily':
        for log in logs:
            if current_date is None or log.logged_date == current_date + timedelta(days=1):
                current_streak += 1
                current_date = log.logged_date
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
                current_date = log.logged_date
        max_streak = max(max_streak, current_streak)
    else:
        max_streak = len(logs)
    
    return max_streak
