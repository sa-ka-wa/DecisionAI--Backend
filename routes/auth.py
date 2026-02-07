from flask import Blueprint, request, jsonify
from controllers.auth_controller import (
    register_user, login_user, get_current_user,
    update_user_profile, update_user_preferences,
    refresh_access_token, logout_user,
    request_password_reset, reset_password
)
from middleware.auth_middleware import jwt_required, validate_request
from utils.validators import (
    RegisterSchema, LoginSchema,
    UpdateProfileSchema, UpdatePreferencesSchema,
    PasswordResetSchema
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@validate_request(RegisterSchema())
def register():
    """Register a new user"""
    return register_user(request.validated_data)

@auth_bp.route('/login', methods=['POST'])
@validate_request(LoginSchema())
def login():
    """Login user"""
    return login_user(request.validated_data)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    """Get current user profile"""
    return get_current_user(request.user)

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
@validate_request(UpdateProfileSchema())
def update_profile():
    """Update user profile"""
    return update_user_profile(request.user, request.validated_data)

@auth_bp.route('/preferences', methods=['PUT'])
@jwt_required
@validate_request(UpdatePreferencesSchema())
def update_preferences():
    """Update user preferences"""
    return update_user_preferences(request.user, request.validated_data)

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    refresh_token = request.json.get('refresh_token')
    return refresh_access_token(refresh_token)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """Logout user"""
    return logout_user(request.user)

@auth_bp.route('/password/reset', methods=['POST'])
@validate_request(PasswordResetSchema())
def request_reset():
    """Request password reset"""
    return request_password_reset(request.validated_data)

@auth_bp.route('/password/reset/<token>', methods=['POST'])
def reset(token):
    """Reset password with token"""
    data = request.get_json()
    return reset_password(token, data.get('password'))

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    """Verify email address"""
    # TODO: Implement email verification
    return jsonify({
        'success': True,
        'message': 'Email verification endpoint'
    })