"""
Calendar routes blueprint.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Habit, HabitLog
from datetime import datetime, date, timedelta
import calendar

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@calendar_bp.route('/<int:year>/<int:month>', methods=['GET'])
@login_required
def get_calendar_month(year, month):
    """Get calendar view for a specific month."""
    # Validate month
    if month < 1 or month > 12:
        return jsonify({'error': 'Invalid month'}), 400
    
    # Get first and last day of month
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    
    # Get all logs for this month
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= first_day,
        HabitLog.logged_date <= last_day
    ).all()
    
    # Build calendar data
    cal_data = {}
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        current_date = date(year, month, day)
        date_key = current_date.isoformat()
        
        # Get logs for this day
        day_logs = [log for log in logs if log.logged_date == current_date]
        
        cal_data[date_key] = {
            'date': date_key,
            'day': day,
            'logs_count': len(day_logs),
            'has_activity': len(day_logs) > 0,
            'logs': [log.to_dict() for log in day_logs]
        }
    
    return jsonify({
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'calendar': cal_data
    }), 200

@calendar_bp.route('/date/<string:target_date>', methods=['GET'])
@login_required
def get_date_details(target_date):
    """Get all activities for a specific date."""
    try:
        target_date_obj = datetime.fromisoformat(target_date).date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Get all logs for this date
    logs = HabitLog.query.filter_by(
        user_id=current_user.id,
        logged_date=target_date_obj
    ).order_by(HabitLog.logged_time.desc()).all()
    
    # Group by habit
    habits_data = {}
    for log in logs:
        habit_id = log.habit_id
        if habit_id not in habits_data:
            habit = Habit.query.get(habit_id)
            habits_data[habit_id] = {
                'habit': habit.to_dict(),
                'logs': []
            }
        habits_data[habit_id]['logs'].append(log.to_dict())
    
    return jsonify({
        'date': target_date,
        'day_of_week': target_date_obj.strftime('%A'),
        'activities': list(habits_data.values()),
        'total_logs': len(logs)
    }), 200

@calendar_bp.route('/heatmap', methods=['GET'])
@login_required
def get_heatmap_data():
    """Get heatmap data for the past 365 days."""
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    
    # Get all logs for the past year
    logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
        HabitLog.logged_date >= start_date,
        HabitLog.logged_date <= end_date
    ).all()
    
    # Group by date
    heatmap = {}
    for log in logs:
        date_key = log.logged_date.isoformat()
        if date_key not in heatmap:
            heatmap[date_key] = 0
        heatmap[date_key] += 1
    
    # Create complete date range
    current_date = start_date
    complete_heatmap = {}
    while current_date <= end_date:
        date_key = current_date.isoformat()
        complete_heatmap[date_key] = heatmap.get(date_key, 0)
        current_date += timedelta(days=1)
    
    return jsonify({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'heatmap': complete_heatmap
    }), 200

@calendar_bp.route('/week/<int:year>/<int:week>', methods=['GET'])
@login_required
def get_calendar_week(year, week):
    """Get calendar view for a specific week."""
    try:
        # Get the first day of the week
        jan4 = date(year, 1, 4)
        week_one_start = jan4 - timedelta(days=jan4.weekday())
        week_start = week_one_start + timedelta(weeks=week - 1)
        week_end = week_start + timedelta(days=6)
        
        # Get all logs for this week
        logs = HabitLog.query.filter_by(user_id=current_user.id).filter(
            HabitLog.logged_date >= week_start,
            HabitLog.logged_date <= week_end
        ).all()
        
        # Build week data
        week_data = {}
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            date_key = current_date.isoformat()
            
            day_logs = [log for log in logs if log.logged_date == current_date]
            
            week_data[date_key] = {
                'date': date_key,
                'day_of_week': current_date.strftime('%A'),
                'logs_count': len(day_logs),
                'logs': [log.to_dict() for log in day_logs]
            }
        
        return jsonify({
            'year': year,
            'week': week,
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'days': week_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Invalid week'}), 400
