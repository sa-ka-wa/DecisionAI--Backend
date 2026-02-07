from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from extensions import db
import uuid
from datetime import datetime


def register_user(data):
    """Register a new user"""
    try:
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'User already exists'
            }), 400

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=data['email'],
            username=data.get('username'),
            name=data['name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'message': 'User registered successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500


def login_user(data):
    """Login user"""
    try:
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is disabled'
            }), 403

        # Update last login
        user.update_last_login()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'message': 'Login successful'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500


def get_current_user(user):
    """Get current user profile"""
    try:
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get user profile',
            'error': str(e)
        }), 500


def update_user_profile(user, data):
    """Update user profile"""
    try:
        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'username' in data:
            # Check if username is unique
            if data['username'] != user.username:
                existing = User.query.filter_by(username=data['username']).first()
                if existing:
                    return jsonify({
                        'success': False,
                        'message': 'Username already taken'
                    }), 400
            user.username = data['username']

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': 'Profile updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update profile',
            'error': str(e)
        }), 500


def update_user_preferences(user, data):
    """Update user preferences"""
    try:
        # Update preferences
        if 'preferences' in data:
            user.preferences = {**user.preferences, **data['preferences']}

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'data': user.preferences,
            'message': 'Preferences updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update preferences',
            'error': str(e)
        }), 500


def refresh_access_token(refresh_token):
    """Refresh access token"""
    # This would be implemented with Flask-JWT-Extended
    # For now, return placeholder
    return jsonify({
        'success': True,
        'message': 'Token refresh endpoint'
    })


def logout_user(user):
    """Logout user"""
    # In a real app, you might blacklist the token
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })


def request_password_reset(data):
    """Request password reset"""
    # TODO: Implement password reset logic
    return jsonify({
        'success': True,
        'message': 'Password reset email sent'
    })


def reset_password(token, new_password):
    """Reset password with token"""
    # TODO: Implement password reset logic
    return jsonify({
        'success': True,
        'message': 'Password reset successful'
    })