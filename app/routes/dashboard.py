"""
Dashboard routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Habit, HabitLog
from datetime import datetime, date, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('', methods=['GET'])
@login_required
def get_dashboard():
    """Get dashboard data for current user."""
    today = date.today()
    
    # Get active habits
    active_habits = Habit.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).count()
    
    # Get today's logs count
    today_logs_count = HabitLog.query.filter_by(
        user_id=current_user.id,
        logged_date=today
    ).count()
    
    # Get total habits
    total_habits = Habit.query.filter_by(user_id=current_user.id).count()
    
    # Get total logs
    total_logs = HabitLog.query.filter_by(user_id=current_user.id).count()
    
    # Get recent activities (last 10)
    recent_logs = HabitLog.query.filter_by(user_id=current_user.id).order_by(
        HabitLog.logged_date.desc(),
        HabitLog.logged_time.desc()
    ).limit(10).all()
    
    # Get favorite habits
    favorite_habits = Habit.query.filter_by(
        user_id=current_user.id,
        is_favorite=True,
        status='active'
    ).all()
    
    # Calculate streaks
    all_habits = Habit.query.filter_by(user_id=current_user.id).all()
    streaks = []
    
    for habit in all_habits:
        current_streak = calculate_current_streak(habit)
        longest_streak = calculate_longest_streak(habit)
        streaks.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'current_streak': current_streak,
            'longest_streak': longest_streak
        })
    
    return jsonify({
        'today': today.isoformat(),
        'active_habits': active_habits,
        'total_habits': total_habits,
        'total_logs': total_logs,
        'today_logs_count': today_logs_count,
        'favorite_habits': [habit.to_dict() for habit in favorite_habits],
        'recent_activities': [log.to_dict() for log in recent_logs],
        'streaks': streaks
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
    
    # Check based on habit frequency
    if habit.frequency == 'daily':
        for log in logs:
            if log.logged_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
    elif habit.frequency == 'weekly':
        current_week = today.isocalendar()[1]
        current_year = today.isocalendar()[0]
        
        for log in logs:
            log_week = log.logged_date.isocalendar()[1]
            log_year = log.logged_date.isocalendar()[0]
            
            if log_year == current_year and log_week == current_week:
                streak += 1
                current_week -= 1
                if current_week == 0:
                    current_week = 52
                    current_year -= 1
            else:
                break
    elif habit.frequency == 'monthly':
        current_month = today.month
        current_year = today.year
        
        for log in logs:
            if log.logged_date.month == current_month and log.logged_date.year == current_year:
                streak += 1
                current_month -= 1
                if current_month == 0:
                    current_month = 12
                    current_year -= 1
            else:
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
        # For weekly/monthly, just count occurrences in different periods
        max_streak = len(logs)
    
    return max_streak

@dashboard_bp.route('/weekly-progress', methods=['GET'])
@login_required
def get_weekly_progress():
    """Get this week's progress."""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get all logs for this week
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= start_of_week,
        HabitLog.logged_date <= end_of_week
    ).all()
    
    # Group by day
    daily_data = {}
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        daily_data[current_date.isoformat()] = {
            'date': current_date.isoformat(),
            'day': current_date.strftime('%A'),
            'logs_count': 0
        }
    
    for log in logs:
        date_key = log.logged_date.isoformat()
        if date_key in daily_data:
            daily_data[date_key]['logs_count'] += 1
    
    return jsonify({
        'week_start': start_of_week.isoformat(),
        'week_end': end_of_week.isoformat(),
        'daily_progress': list(daily_data.values())
    }), 200

@dashboard_bp.route('/monthly-progress', methods=['GET'])
@login_required
def get_monthly_progress():
    """Get this month's progress."""
    today = date.today()
    start_of_month = today.replace(day=1)
    
    # Get last day of month
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    # Get all logs for this month
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= start_of_month,
        HabitLog.logged_date <= end_of_month
    ).all()
    
    return jsonify({
        'month': today.strftime('%Y-%m'),
        'total_logs': len(logs),
        'logs': [log.to_dict() for log in logs]
    }), 200
