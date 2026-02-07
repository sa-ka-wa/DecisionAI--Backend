from flask import Blueprint, request, jsonify
from controllers.task_controller import (
    create_task, get_tasks, get_task,
    update_task, delete_task, update_task_status,
    update_task_progress, get_tasks_by_category,
    get_tasks_by_priority, get_overdue_tasks,
    get_upcoming_tasks, get_task_insights,
    bulk_create_tasks, bulk_delete_tasks
)
from middleware.auth_middleware import jwt_required, validate_request
from utils.validators import (
    CreateTaskSchema, UpdateTaskSchema,
    TaskStatusSchema, TaskProgressSchema,
    BulkTaskSchema
)

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('', methods=['POST'])
@jwt_required
@validate_request(CreateTaskSchema())
def create():
    """Create a new task"""
    return create_task(request.user, request.validated_data)


@tasks_bp.route('', methods=['GET'])
@jwt_required
def list_tasks():
    """Get all tasks with filters"""
    filters = {
        'status': request.args.get('status'),
        'priority': request.args.get('priority'),
        'category': request.args.get('category'),
        'tags': request.args.get('tags'),
        'due_before': request.args.get('due_before'),
        'due_after': request.args.get('due_after'),
        'search': request.args.get('search'),
    }
    sort_by = request.args.get('sort_by', 'priority')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))

    return get_tasks(request.user, filters, sort_by, order, page, limit)


@tasks_bp.route('/<task_id>', methods=['GET'])
@jwt_required
def get_single(task_id):
    """Get a specific task"""
    return get_task(request.user, task_id)


@tasks_bp.route('/<task_id>', methods=['PUT'])
@jwt_required
@validate_request(UpdateTaskSchema())
def update(task_id):
    """Update a task"""
    return update_task(request.user, task_id, request.validated_data)


@tasks_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required
def delete(task_id):
    """Delete a task"""
    return delete_task(request.user, task_id)


@tasks_bp.route('/<task_id>/status', methods=['PATCH'])
@jwt_required
@validate_request(TaskStatusSchema())
def update_status(task_id):
    """Update task status"""
    return update_task_status(request.user, task_id, request.validated_data)


@tasks_bp.route('/<task_id>/progress', methods=['PATCH'])
@jwt_required
@validate_request(TaskProgressSchema())
def update_progress(task_id):
    """Update task progress"""
    return update_task_progress(request.user, task_id, request.validated_data)


@tasks_bp.route('/category/<category>', methods=['GET'])
@jwt_required
def by_category(category):
    """Get tasks by category"""
    return get_tasks_by_category(request.user, category)


@tasks_bp.route('/priority/<int:priority>', methods=['GET'])
@jwt_required
def by_priority(priority):
    """Get tasks by priority level"""
    return get_tasks_by_priority(request.user, priority)


@tasks_bp.route('/overdue', methods=['GET'])
@jwt_required
def overdue():
    """Get overdue tasks"""
    return get_overdue_tasks(request.user)


@tasks_bp.route('/upcoming', methods=['GET'])
@jwt_required
def upcoming():
    """Get upcoming tasks (next 7 days)"""
    return get_upcoming_tasks(request.user)


@tasks_bp.route('/<task_id>/insights', methods=['GET'])
@jwt_required
def insights(task_id):
    """Get AI insights for a task"""
    return get_task_insights(request.user, task_id)


@tasks_bp.route('/bulk', methods=['POST'])
@jwt_required
@validate_request(BulkTaskSchema())
def bulk_create():
    """Bulk create tasks"""
    return bulk_create_tasks(request.user, request.validated_data['tasks'])


@tasks_bp.route('/bulk', methods=['DELETE'])
@jwt_required
def bulk_delete():
    """Bulk delete tasks"""
    task_ids = request.json.get('task_ids', [])
    return bulk_delete_tasks(request.user, task_ids)