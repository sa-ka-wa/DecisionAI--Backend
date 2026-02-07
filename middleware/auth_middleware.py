from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User
import jwt
from datetime import datetime


def jwt_required(fn):
    """Custom JWT required decorator"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            # Get user from database
            user = User.query.get(current_user_id)
            if not user or not user.is_active:
                return jsonify({
                    'success': False,
                    'message': 'User not found or inactive'
                }), 401

            # Add user to request context
            request.user = user
            return fn(*args, **kwargs)

        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token',
                'error': str(e)
            }), 401

    return wrapper


def admin_required(fn):
    """Require admin role"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            user = User.query.get(current_user_id)
            if not user or user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Admin access required'
                }), 403

            request.user = user
            return fn(*args, **kwargs)

        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Authentication failed',
                'error': str(e)
            }), 401

    return wrapper


def validate_request(schema):
    """Validate request data against schema"""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                errors = schema.validate(data) if schema else {}

                if errors:
                    return jsonify({
                        'success': False,
                        'message': 'Validation failed',
                        'errors': errors
                    }), 400

                # Add validated data to request
                request.validated_data = data
                return fn(*args, **kwargs)

            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Invalid request data',
                    'error': str(e)
                }), 400

        return wrapper

    return decorator


def rate_limit(requests_per_minute=60):
    """Simple rate limiting decorator"""
    from collections import defaultdict
    from time import time

    requests = defaultdict(list)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time()

            # Clean old requests
            requests[client_ip] = [
                req_time for req_time in requests[client_ip]
                if current_time - req_time < 60
            ]

            # Check rate limit
            if len(requests[client_ip]) >= requests_per_minute:
                return jsonify({
                    'success': False,
                    'message': 'Rate limit exceeded. Try again later.'
                }), 429

            # Add current request
            requests[client_ip].append(current_time)

            return fn(*args, **kwargs)

        return wrapper

    return decorator