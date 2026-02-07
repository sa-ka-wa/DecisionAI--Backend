# controllers/task_controller.py
from flask import jsonify, request
from models.task import Task, TaskHistory
from models.user import User
from extensions import db
from utils.ai_helper import AIHelper
from datetime import datetime, timedelta
import uuid
from sqlalchemy import and_, or_

# Initialize AI Helper
ai_helper = AIHelper()


def create_task(user, data):
    """Create a new task"""
    try:
        # Generate AI insights if enabled
        ai_insights = {}
        if user.preferences.get('ai_enabled', True):
            ai_insights = ai_helper.analyze_task(data.get('description', ''))

        task = Task(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title=data['title'],
            description=data.get('description', ''),
            category=data.get('category', 'Other'),
            priority=data.get('priority', 3),
            impact=data.get('impact', 5),
            status=data.get('status', 'pending'),
            progress=data.get('progress', 0),
            due_date=data['due_date'],
            tags=data.get('tags', []),
            complexity=data.get('complexity', 3),
            estimated_hours=data.get('estimated_hours', 1.0),
            ai_insights=ai_insights
        )

        db.session.add(task)

        # Log history
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='created',
            changes={'from': None, 'to': task.to_dict()}
        )
        db.session.add(history)

        db.session.commit()

        # Update user stats
        user.update_stats('task_created')

        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task created successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to create task',
            'error': str(e)
        }), 500


def get_tasks(user, filters=None, sort_by='priority', order='asc', page=1, limit=20):
    """Get tasks with filters"""
    try:
        # Build query
        query = Task.query.filter_by(user_id=user.id)

        # Apply filters
        if filters:
            if filters.get('status'):
                query = query.filter(Task.status == filters['status'])
            if filters.get('priority'):
                query = query.filter(Task.priority == int(filters['priority']))
            if filters.get('category'):
                query = query.filter(Task.category == filters['category'])
            if filters.get('due_before'):
                due_date = datetime.fromisoformat(filters['due_before'].replace('Z', '+00:00'))
                query = query.filter(Task.due_date <= due_date)
            if filters.get('due_after'):
                due_date = datetime.fromisoformat(filters['due_after'].replace('Z', '+00:00'))
                query = query.filter(Task.due_date >= due_date)
            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Task.title.ilike(search_term),
                        Task.description.ilike(search_term)
                    )
                )

        # Apply sorting
        sort_column = getattr(Task, sort_by, Task.priority)
        if order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Pagination
        paginated = query.paginate(page=page, per_page=limit, error_out=False)

        tasks_data = [task.to_dict() for task in paginated.items]

        return jsonify({
            'success': True,
            'data': tasks_data,
            'pagination': {
                'page': paginated.page,
                'per_page': paginated.per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch tasks',
            'error': str(e)
        }), 500


def get_task(user, task_id):
    """Get single task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'data': task.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch task',
            'error': str(e)
        }), 500


def update_task(user, task_id, data):
    """Update a task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        # Store old values for history
        old_values = task.to_dict()

        # Update fields
        update_fields = [
            'title', 'description', 'category', 'priority',
            'impact', 'status', 'progress', 'due_date',
            'tags', 'complexity', 'estimated_hours'
        ]

        for field in update_fields:
            if field in data:
                setattr(task, field, data[field])

        task.updated_at = datetime.utcnow()

        # Update AI insights if description changed
        if 'description' in data and user.preferences.get('ai_enabled', True):
            task.ai_insights = ai_helper.analyze_task(data['description'])

        # Log history
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='updated',
            changes={'from': old_values, 'to': task.to_dict()}
        )
        db.session.add(history)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update task',
            'error': str(e)
        }), 500


def delete_task(user, task_id):
    """Delete a task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        # Log history before deletion
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='deleted',
            changes={'deleted_task': task.to_dict()}
        )
        db.session.add(history)

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to delete task',
            'error': str(e)
        }), 500


def update_task_status(user, task_id, data):
    """Update task status"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        old_status = task.status
        new_status = data['status']

        task.status = new_status
        task.updated_at = datetime.utcnow()

        # Handle status-specific updates
        if new_status == 'completed' and old_status != 'completed':
            task.progress = 100
            task.completed_at = datetime.utcnow()
            user.update_stats('task_completed', task.impact)
        elif new_status == 'in-progress' and old_status != 'in-progress':
            task.started_at = datetime.utcnow()

        # Log history
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='status_updated',
            changes={'from': old_status, 'to': new_status}
        )
        db.session.add(history)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task status updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update task status',
            'error': str(e)
        }), 500


def update_task_progress(user, task_id, data):
    """Update task progress"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        old_progress = task.progress
        new_progress = data['progress']

        if not 0 <= new_progress <= 100:
            return jsonify({
                'success': False,
                'message': 'Progress must be between 0 and 100'
            }), 400

        task.progress = new_progress
        task.updated_at = datetime.utcnow()

        # Auto-update status based on progress
        if new_progress == 100:
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            user.update_stats('task_completed', task.impact)
        elif new_progress > 0 and task.status == 'pending':
            task.status = 'in-progress'
            if not task.started_at:
                task.started_at = datetime.utcnow()

        # Log history
        history = TaskHistory(
            task_id=task.id,
            user_id=user.id,
            action='progress_updated',
            changes={'from': old_progress, 'to': new_progress}
        )
        db.session.add(history)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task progress updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update task progress',
            'error': str(e)
        }), 500


def get_tasks_by_category(user, category):
    """Get tasks by category"""
    try:
        tasks = Task.query.filter_by(
            user_id=user.id,
            category=category
        ).order_by(Task.priority).all()

        tasks_data = [task.to_dict() for task in tasks]

        return jsonify({
            'success': True,
            'data': tasks_data,
            'category': category,
            'count': len(tasks_data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch tasks by category',
            'error': str(e)
        }), 500


def get_tasks_by_priority(user, priority):
    """Get tasks by priority level"""
    try:
        if not 1 <= priority <= 5:
            return jsonify({
                'success': False,
                'message': 'Priority must be between 1 and 5'
            }), 400

        tasks = Task.query.filter_by(
            user_id=user.id,
            priority=priority
        ).order_by(Task.due_date).all()

        tasks_data = [task.to_dict() for task in tasks]

        return jsonify({
            'success': True,
            'data': tasks_data,
            'priority': priority,
            'count': len(tasks_data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch tasks by priority',
            'error': str(e)
        }), 500


def get_overdue_tasks(user):
    """Get overdue tasks"""
    try:
        tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.status != 'completed',
            Task.due_date < datetime.utcnow()
        ).order_by(Task.priority).all()

        tasks_data = [task.to_dict() for task in tasks]

        return jsonify({
            'success': True,
            'data': tasks_data,
            'count': len(tasks_data)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch overdue tasks',
            'error': str(e)
        }), 500


def get_upcoming_tasks(user):
    """Get upcoming tasks (next 7 days)"""
    try:
        seven_days_from_now = datetime.utcnow() + timedelta(days=7)

        tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.status != 'completed',
            Task.due_date >= datetime.utcnow(),
            Task.due_date <= seven_days_from_now
        ).order_by(Task.due_date).all()

        tasks_data = [task.to_dict() for task in tasks]

        return jsonify({
            'success': True,
            'data': tasks_data,
            'count': len(tasks_data),
            'timeframe': 'next_7_days'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch upcoming tasks',
            'error': str(e)
        }), 500


def get_task_insights(user, task_id):
    """Get AI insights for a task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=user.id).first()

        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404

        # Generate fresh AI insights if none exist or if forced
        insights = task.ai_insights
        if not insights or request.args.get('refresh') == 'true':
            if user.preferences.get('ai_enabled', True):
                insights = ai_helper.analyze_task(task.description)
                task.ai_insights = insights
                db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'task_id': task_id,
                'insights': insights,
                'generated_at': datetime.utcnow().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get task insights',
            'error': str(e)
        }), 500


def bulk_create_tasks(user, tasks_data):
    """Bulk create tasks"""
    try:
        created_tasks = []

        for task_data in tasks_data:
            # Generate AI insights if enabled
            ai_insights = {}
            if user.preferences.get('ai_enabled', True):
                ai_insights = ai_helper.analyze_task(task_data.get('description', ''))

            task = Task(
                id=str(uuid.uuid4()),
                user_id=user.id,
                title=task_data['title'],
                description=task_data.get('description', ''),
                category=task_data.get('category', 'Other'),
                priority=task_data.get('priority', 3),
                impact=task_data.get('impact', 5),
                status=task_data.get('status', 'pending'),
                progress=task_data.get('progress', 0),
                due_date=task_data.get('due_date', datetime.utcnow()),
                tags=task_data.get('tags', []),
                complexity=task_data.get('complexity', 3),
                estimated_hours=task_data.get('estimated_hours', 1.0),
                ai_insights=ai_insights
            )

            db.session.add(task)
            created_tasks.append(task)

            # Log history
            history = TaskHistory(
                task_id=task.id,
                user_id=user.id,
                action='created',
                changes={'from': None, 'to': task.to_dict()}
            )
            db.session.add(history)

        db.session.commit()

        # Update user stats
        user.stats['total_tasks'] = user.stats.get('total_tasks', 0) + len(created_tasks)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in created_tasks],
            'message': f'Successfully created {len(created_tasks)} tasks',
            'count': len(created_tasks)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to bulk create tasks',
            'error': str(e)
        }), 500


def bulk_delete_tasks(user, task_ids):
    """Bulk delete tasks"""
    try:
        tasks = Task.query.filter(
            Task.user_id == user.id,
            Task.id.in_(task_ids)
        ).all()

        if not tasks:
            return jsonify({
                'success': False,
                'message': 'No tasks found to delete'
            }), 404

        deleted_ids = []
        for task in tasks:
            # Log history before deletion
            history = TaskHistory(
                task_id=task.id,
                user_id=user.id,
                action='deleted',
                changes={'deleted_task': task.to_dict()}
            )
            db.session.add(history)

            deleted_ids.append(task.id)
            db.session.delete(task)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'deleted_task_ids': deleted_ids,
                'count': len(deleted_ids)
            },
            'message': f'Successfully deleted {len(deleted_ids)} tasks'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to bulk delete tasks',
            'error': str(e)
        }), 500