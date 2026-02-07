# controllers/analytics_controller.py
from flask import jsonify, request
from models.task import Task
from models.user import User
from extensions import db
from utils.ai_helper import AIHelper
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import json
import csv
from io import StringIO

ai_helper = AIHelper()


def get_dashboard_stats(user):
    """Get dashboard statistics"""
    try:
        # Get task counts by status
        total_tasks = Task.query.filter_by(user_id=user.id).count()
        completed_tasks = Task.query.filter_by(user_id=user.id, status='completed').count()
        pending_tasks = Task.query.filter_by(user_id=user.id, status='pending').count()
        in_progress_tasks = Task.query.filter_by(user_id=user.id, status='in-progress').count()

        # Get overdue tasks
        overdue_tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.status != 'completed',
            Task.due_date < datetime.utcnow()
        ).count()

        # Calculate average completion time for completed tasks
        completed_tasks_with_dates = Task.query.filter_by(
            user_id=user.id,
            status='completed'
        ).filter(Task.completed_at.isnot(None), Task.started_at.isnot(None)).all()

        avg_completion_time = 0
        if completed_tasks_with_dates:
            total_hours = sum([
                (task.completed_at - task.started_at).total_seconds() / 3600
                for task in completed_tasks_with_dates
                if task.completed_at and task.started_at
            ])
            avg_completion_time = total_hours / len(completed_tasks_with_dates)

        # Calculate productivity score (0-100)
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            on_time_rate = 100  # Simplified for now
            productivity_score = (completion_rate * 0.6) + (on_time_rate * 0.4)
        else:
            productivity_score = 0

        # Get average impact
        avg_impact = db.session.query(func.avg(Task.impact)).filter_by(
            user_id=user.id
        ).scalar() or 0

        # Get priority distribution
        priority_counts = {}
        for priority in range(1, 6):
            count = Task.query.filter_by(
                user_id=user.id,
                priority=priority
            ).count()
            priority_counts[f'priority_{priority}'] = count

        return jsonify({
            'success': True,
            'data': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'in_progress_tasks': in_progress_tasks,
                'overdue_tasks': overdue_tasks,
                'avg_completion_time': round(avg_completion_time, 2),
                'productivity_score': round(productivity_score, 2),
                'avg_impact': round(avg_impact, 2),
                'priority_distribution': priority_counts,
                'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get dashboard stats',
            'error': str(e)
        }), 500


def get_completion_rate(user, period='week'):
    """Get completion rate over time"""
    try:
        end_date = datetime.utcnow()

        if period == 'week':
            start_date = end_date - timedelta(days=7)
            group_by = 'day'
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
            group_by = 'day'
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
            group_by = 'month'
        else:
            start_date = end_date - timedelta(days=7)
            group_by = 'day'

        # Query for completed tasks in period
        completed_tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.status == 'completed',
            Task.completed_at.between(start_date, end_date)
        ).all()

        # Create timeline data
        timeline_data = []
        current = start_date

        while current <= end_date:
            if group_by == 'day':
                date_key = current.strftime('%Y-%m-%d')
                next_date = current + timedelta(days=1)
            else:  # month
                date_key = current.strftime('%Y-%m')
                next_date = current + timedelta(days=30)

            # Count tasks completed on this day/month
            tasks_on_date = [
                task for task in completed_tasks
                if task.completed_at and (
                        (group_by == 'day' and task.completed_at.date() == current.date()) or
                        (group_by == 'month' and task.completed_at.strftime('%Y-%m') == date_key)
                )
            ]

            timeline_data.append({
                'date': date_key,
                'completed_tasks': len(tasks_on_date),
                'avg_impact': round(
                    sum(task.impact for task in tasks_on_date) / len(tasks_on_date)
                    if tasks_on_date else 0, 2
                )
            })

            current = next_date

        # Calculate completion rate
        total_tasks_in_period = Task.query.filter(
            Task.user_id == user.id,
            Task.created_at.between(start_date, end_date)
        ).count()

        completion_rate = round(
            (len(completed_tasks) / total_tasks_in_period * 100)
            if total_tasks_in_period > 0 else 0, 2
        )

        return jsonify({
            'success': True,
            'data': {
                'timeline': timeline_data,
                'period': period,
                'total_completed': len(completed_tasks),
                'total_created': total_tasks_in_period,
                'completion_rate': completion_rate,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get completion rate',
            'error': str(e)
        }), 500


def get_category_breakdown(user):
    """Get breakdown of tasks by category"""
    try:
        # Get all tasks grouped by category
        tasks_by_category = db.session.query(
            Task.category,
            func.count(Task.id).label('count'),
            func.avg(Task.impact).label('avg_impact'),
            func.avg(Task.priority).label('avg_priority')
        ).filter_by(
            user_id=user.id
        ).group_by(
            Task.category
        ).all()

        total_tasks = Task.query.filter_by(user_id=user.id).count()

        categories = []
        counts = []
        percentages = []
        avg_impacts = []

        for category, count, avg_impact, avg_priority in tasks_by_category:
            categories.append(category)
            counts.append(count)
            percentages.append(round((count / total_tasks * 100) if total_tasks > 0 else 0, 2))
            avg_impacts.append(round(avg_impact or 0, 2))

        return jsonify({
            'success': True,
            'data': {
                'categories': categories,
                'counts': counts,
                'percentages': percentages,
                'avg_impacts': avg_impacts,
                'total_tasks': total_tasks
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get category breakdown',
            'error': str(e)
        }), 500


def get_impact_analysis(user):
    """Get impact analysis of tasks"""
    try:
        # Get tasks grouped by impact level
        impact_levels = {}
        for impact in range(1, 11):
            count = Task.query.filter_by(user_id=user.id, impact=impact).count()
            impact_levels[str(impact)] = count

        # Get high impact tasks (impact >= 8)
        high_impact_tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.impact >= 8
        ).order_by(Task.priority).limit(10).all()

        # Calculate impact trends
        recent_tasks = Task.query.filter_by(
            user_id=user.id
        ).order_by(Task.created_at.desc()).limit(20).all()

        recent_avg_impact = round(
            sum(task.impact for task in recent_tasks) / len(recent_tasks)
            if recent_tasks else 0, 2
        )

        # Overall average impact
        overall_avg_impact = db.session.query(
            func.avg(Task.impact)
        ).filter_by(user_id=user.id).scalar() or 0

        return jsonify({
            'success': True,
            'data': {
                'impact_distribution': impact_levels,
                'high_impact_tasks': [
                    {
                        'id': task.id,
                        'title': task.title,
                        'impact': task.impact,
                        'priority': task.priority,
                        'status': task.status
                    }
                    for task in high_impact_tasks
                ],
                'recent_avg_impact': recent_avg_impact,
                'overall_avg_impact': round(overall_avg_impact, 2),
                'impact_trend': 'increasing' if recent_avg_impact > overall_avg_impact else 'decreasing' if recent_avg_impact < overall_avg_impact else 'stable'
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get impact analysis',
            'error': str(e)
        }), 500


def get_priority_distribution(user):
    """Get distribution of tasks by priority level"""
    try:
        priority_data = []
        for priority in range(1, 6):
            tasks = Task.query.filter_by(user_id=user.id, priority=priority).all()

            if tasks:
                avg_impact = sum(task.impact for task in tasks) / len(tasks)
                completion_rate = sum(1 for task in tasks if task.status == 'completed') / len(tasks) * 100
            else:
                avg_impact = 0
                completion_rate = 0

            priority_data.append({
                'priority_level': priority,
                'count': len(tasks),
                'avg_impact': round(avg_impact, 2),
                'completion_rate': round(completion_rate, 2),
                'avg_completion_time': 0  # Simplified for now
            })

        return jsonify({
            'success': True,
            'data': {
                'priorities': priority_data,
                'total_tasks': sum(item['count'] for item in priority_data)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get priority distribution',
            'error': str(e)
        }), 500


def get_timeline_data(user):
    """Get timeline data for task completion"""
    try:
        # Get last 30 days of data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)

        timeline = []
        current = start_date

        while current <= end_date:
            next_day = current + timedelta(days=1)

            # Tasks created on this day
            created = Task.query.filter(
                Task.user_id == user.id,
                Task.created_at >= current,
                Task.created_at < next_day
            ).count()

            # Tasks completed on this day
            completed = Task.query.filter(
                Task.user_id == user.id,
                Task.status == 'completed',
                Task.completed_at >= current,
                Task.completed_at < next_day
            ).count()

            timeline.append({
                'date': current.strftime('%Y-%m-%d'),
                'created': created,
                'completed': completed,
                'net_change': completed - created
            })

            current = next_day

        return jsonify({
            'success': True,
            'data': {
                'timeline': timeline,
                'period': '30_days',
                'total_created': sum(day['created'] for day in timeline),
                'total_completed': sum(day['completed'] for day in timeline),
                'avg_daily_completed': round(
                    sum(day['completed'] for day in timeline) / len(timeline), 2
                ) if timeline else 0
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get timeline data',
            'error': str(e)
        }), 500


def get_performance_metrics(user):
    """Get performance metrics and trends"""
    try:
        # Calculate various performance metrics
        total_tasks = Task.query.filter_by(user_id=user.id).count()
        completed_tasks = Task.query.filter_by(user_id=user.id, status='completed').count()

        # Efficiency metrics
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
        else:
            completion_rate = 0

        # Average time to completion (for completed tasks)
        completed_with_dates = Task.query.filter_by(
            user_id=user.id,
            status='completed'
        ).filter(Task.completed_at.isnot(None), Task.started_at.isnot(None)).all()

        avg_time_to_completion = 0
        if completed_with_dates:
            total_time = sum([
                (task.completed_at - task.started_at).total_seconds() / 3600
                for task in completed_with_dates
            ])
            avg_time_to_completion = total_time / len(completed_with_dates)

        # Priority accuracy (how many high priority tasks completed)
        high_priority_completed = Task.query.filter_by(
            user_id=user.id,
            status='completed',
            priority=1
        ).count()

        high_priority_total = Task.query.filter_by(
            user_id=user.id,
            priority=1
        ).count()

        priority_accuracy = (high_priority_completed / high_priority_total * 100) if high_priority_total > 0 else 0

        # Impact achievement
        total_impact = db.session.query(func.sum(Task.impact)).filter_by(
            user_id=user.id,
            status='completed'
        ).scalar() or 0

        return jsonify({
            'success': True,
            'data': {
                'completion_rate': round(completion_rate, 2),
                'avg_time_to_completion': round(avg_time_to_completion, 2),
                'priority_accuracy': round(priority_accuracy, 2),
                'total_impact_achieved': round(total_impact, 2),
                'efficiency_score': round(
                    completion_rate * 0.4 + priority_accuracy * 0.3 + (100 - min(avg_time_to_completion, 100)) * 0.3,
                    2),
                'tasks_completed': completed_tasks,
                'tasks_pending': total_tasks - completed_tasks
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get performance metrics',
            'error': str(e)
        }), 500


def get_productivity_score(user):
    """Get user productivity score"""
    try:
        # Get various metrics
        total_tasks = Task.query.filter_by(user_id=user.id).count()
        completed_tasks = Task.query.filter_by(user_id=user.id, status='completed').count()

        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Calculate on-time completion rate
        on_time_tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.status == 'completed',
            Task.completed_at <= Task.due_date
        ).count()

        on_time_rate = (on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0

        # Calculate impact efficiency
        total_impact = db.session.query(func.sum(Task.impact)).filter_by(
            user_id=user.id
        ).scalar() or 0

        completed_impact = db.session.query(func.sum(Task.impact)).filter_by(
            user_id=user.id,
            status='completed'
        ).scalar() or 0

        impact_efficiency = (completed_impact / total_impact * 100) if total_impact > 0 else 0

        # Calculate consistency (tasks completed per day over last 7 days)
        last_week = datetime.utcnow() - timedelta(days=7)
        daily_completions = []

        for i in range(7):
            day_start = last_week + timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            completions = Task.query.filter(
                Task.user_id == user.id,
                Task.status == 'completed',
                Task.completed_at >= day_start,
                Task.completed_at < day_end
            ).count()

            daily_completions.append(completions)

        consistency_score = (sum(1 for d in daily_completions if d > 0) / 7 * 100) if daily_completions else 0

        # Calculate overall productivity score (0-100)
        productivity_score = (
                completion_rate * 0.3 +
                on_time_rate * 0.25 +
                impact_efficiency * 0.25 +
                consistency_score * 0.2
        )

        return jsonify({
            'success': True,
            'data': {
                'productivity_score': round(productivity_score, 2),
                'components': {
                    'completion_rate': round(completion_rate, 2),
                    'on_time_rate': round(on_time_rate, 2),
                    'impact_efficiency': round(impact_efficiency, 2),
                    'consistency_score': round(consistency_score, 2)
                },
                'daily_completions': daily_completions,
                'level': 'High' if productivity_score >= 80 else 'Medium' if productivity_score >= 60 else 'Low',
                'recommendations': self._get_productivity_recommendations(productivity_score, completion_rate,
                                                                          on_time_rate)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get productivity score',
            'error': str(e)
        }), 500

    def _get_productivity_recommendations(self, score, completion_rate, on_time_rate):
        """Get productivity improvement recommendations"""
        recommendations = []

        if completion_rate < 60:
            recommendations.append("Focus on completing more tasks - aim for at least 60% completion rate")

        if on_time_rate < 70:
            recommendations.append("Improve time management - try setting realistic deadlines")

        if score < 60:
            recommendations.append("Break larger tasks into smaller, manageable subtasks")
            recommendations.append("Use the priority system to focus on high-impact tasks first")

        return recommendations


def get_ai_recommendations(user):
    """Get AI-powered task recommendations"""
    try:
        # Get user's tasks
        tasks = Task.query.filter_by(user_id=user.id).all()

        if not tasks:
            return jsonify({
                'success': True,
                'data': {
                    'focus_areas': ["Start by creating your first task"],
                    'quick_wins': [],
                    'risk_alerts': [],
                    'optimization_tips': ["Add tasks to get personalized recommendations"],
                    'efficiency_score': 0
                }
            })

        # Use AI helper for recommendations
        recommendations = ai_helper.generate_recommendations(tasks)

        # Add specific task-based recommendations
        pending_tasks = [t for t in tasks if t.status == 'pending']
        high_priority_tasks = [t for t in pending_tasks if t.priority <= 2]
        high_impact_tasks = [t for t in pending_tasks if t.impact >= 8]

        if high_priority_tasks:
            recommendations['specific_tasks'] = [
                {
                    'id': task.id,
                    'title': task.title,
                    'reason': 'High priority',
                    'estimated_time': task.estimated_hours
                }
                for task in high_priority_tasks[:3]
            ]

        return jsonify({
            'success': True,
            'data': recommendations
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get AI recommendations',
            'error': str(e)
        }), 500


def get_optimization_tips(user):
    """Get optimization tips"""
    try:
        tasks = Task.query.filter_by(user_id=user.id).all()

        tips = []

        # Analyze task patterns
        if tasks:
            # Check for overdue tasks
            overdue_count = sum(1 for t in tasks if t.is_overdue)
            if overdue_count > 0:
                tips.append(f"You have {overdue_count} overdue tasks. Consider rescheduling or breaking them down.")

            # Check for task clustering
            categories = {}
            for task in tasks:
                categories[task.category] = categories.get(task.category, 0) + 1

            if len(categories) > 5:
                tips.append("You have tasks in many different categories. Consider consolidating similar tasks.")

            # Check for estimated vs actual (simplified)
            long_tasks = [t for t in tasks if t.estimated_hours > 8]
            if long_tasks:
                tips.append(
                    f"You have {len(long_tasks)} tasks estimated over 8 hours. Break them into smaller subtasks.")

        # Add general tips
        tips.extend([
            "Schedule 2-3 high-impact tasks per day for maximum productivity",
            "Review and update task priorities weekly",
            "Use time blocking for focused work sessions",
            "Delegate or eliminate low-impact tasks when possible"
        ])

        return jsonify({
            'success': True,
            'data': {
                'tips': tips[:5],  # Limit to 5 tips
                'generated_at': datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get optimization tips',
            'error': str(e)
        }), 500


def get_risk_analysis(user):
    """Get risk analysis"""
    try:
        tasks = Task.query.filter_by(user_id=user.id).all()

        risks = []

        if tasks:
            # Overdue risk
            overdue_tasks = [t for t in tasks if t.is_overdue]
            if overdue_tasks:
                risks.append({
                    'type': 'overdue',
                    'severity': 'high',
                    'message': f'{len(overdue_tasks)} tasks are overdue',
                    'tasks': [t.title for t in overdue_tasks[:3]]
                })

            # High priority pending risk
            high_priority_pending = [t for t in tasks if t.priority == 1 and t.status == 'pending']
            if high_priority_pending:
                risks.append({
                    'type': 'high_priority_pending',
                    'severity': 'critical',
                    'message': f'{len(high_priority_pending)} critical priority tasks pending',
                    'tasks': [t.title for t in high_priority_pending[:3]]
                })

            # Upcoming deadline risk
            next_week = datetime.utcnow() + timedelta(days=7)
            upcoming_deadlines = [t for t in tasks if
                                  t.due_date and t.due_date <= next_week and t.status != 'completed']
            if upcoming_deadlines:
                risks.append({
                    'type': 'upcoming_deadlines',
                    'severity': 'medium',
                    'message': f'{len(upcoming_deadlines)} tasks due within 7 days',
                    'tasks': [t.title for t in upcoming_deadlines[:3]]
                })

        # Calculate risk score (0-100, higher is more risky)
        risk_score = min(100, len(risks) * 20)

        return jsonify({
            'success': True,
            'data': {
                'risks': risks,
                'risk_score': risk_score,
                'risk_level': 'High' if risk_score >= 70 else 'Medium' if risk_score >= 40 else 'Low',
                'recommendations': [
                                       'Address overdue tasks immediately',
                                       'Focus on critical priority tasks',
                                       'Review upcoming deadlines'
                                   ][:len(risks)]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get risk analysis',
            'error': str(e)
        }), 500


def export_analytics_data(user, format_type='json'):
    """Export analytics data"""
    try:
        # Get all tasks for the user
        tasks = Task.query.filter_by(user_id=user.id).all()

        if format_type == 'csv':
            # Create CSV data
            output = StringIO()
            writer = csv.writer(output)

            # Write header
            writer.writerow([
                'ID', 'Title', 'Category', 'Priority', 'Impact',
                'Status', 'Progress', 'Due Date', 'Created At', 'Completed At'
            ])

            # Write task data
            for task in tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    task.category,
                    task.priority,
                    task.impact,
                    task.status,
                    f'{task.progress}%',
                    task.due_date.isoformat() if task.due_date else '',
                    task.created_at.isoformat() if task.created_at else '',
                    task.completed_at.isoformat() if task.completed_at else ''
                ])

            csv_data = output.getvalue()
            output.close()

            return jsonify({
                'success': True,
                'data': csv_data,
                'format': 'csv',
                'filename': f'decisionai_export_{datetime.utcnow().strftime("%Y%m%d")}.csv'
            })

        else:  # Default to JSON
            tasks_data = [task.to_dict() for task in tasks]

            # Add analytics summary
            summary = {
                'total_tasks': len(tasks),
                'completed_tasks': len([t for t in tasks if t.status == 'completed']),
                'pending_tasks': len([t for t in tasks if t.status == 'pending']),
                'export_date': datetime.utcnow().isoformat(),
                'user': user.email
            }

            export_data = {
                'summary': summary,
                'tasks': tasks_data
            }

            return jsonify({
                'success': True,
                'data': export_data,
                'format': 'json'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to export analytics data',
            'error': str(e)
        }), 500