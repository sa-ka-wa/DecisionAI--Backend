# utils/validators.py
from marshmallow import Schema, fields, validate, validates, ValidationError, post_load, EXCLUDE
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timezone
import re


class RegisterSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True, error_messages={'required': 'Email is required'})
    username = fields.String(required=False, validate=validate.Length(min=3, max=50))
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    password = fields.String(required=True, validate=validate.Length(min=6, max=100))

    @validates('email')
    def validate_email(self, value):
        try:
            validate_email(value, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValidationError(str(e))

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters')
        # Add more password validation if needed


class LoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UpdateProfileSchema(Schema):
    """Schema for updating user profile"""
    name = fields.String(validate=validate.Length(min=2, max=100))
    username = fields.String(validate=validate.Length(min=3, max=50))
    email = fields.Email()


class UpdatePreferencesSchema(Schema):
    """Schema for updating user preferences"""
    preferences = fields.Dict()


class PasswordResetSchema(Schema):
    """Schema for password reset request"""
    email = fields.Email(required=True)


class CreateTaskSchema(Schema):
    """Schema for creating a task"""
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=1000))
    category = fields.String(validate=validate.Length(max=50))
    priority = fields.Integer(validate=validate.Range(min=1, max=5))
    impact = fields.Integer(validate=validate.Range(min=1, max=10))
    status = fields.String(validate=validate.OneOf(['pending', 'in-progress', 'completed', 'blocked']))
    progress = fields.Integer(validate=validate.Range(min=0, max=100))
    due_date = fields.DateTime(required=True)
    tags = fields.List(fields.String())
    complexity = fields.Integer(validate=validate.Range(min=1, max=5))
    estimated_hours = fields.Float(validate=validate.Range(min=0.1, max=1000))

    class Meta:
        unknown = EXCLUDE

    @validates('due_date')
    def validate_due_date(self, value):
        """
        Ensure due_date is in the future
        """
        # Get current time in UTC (timezone-aware)
        now = datetime.now(timezone.utc)

        # Convert input to UTC timezone-aware datetime
        # If input is naive, treat it as UTC
        if value.tzinfo is None:
            value_utc = value.replace(tzinfo=timezone.utc)
        else:
            value_utc = value.astimezone(timezone.utc)

        # Validate: due_date must be in the future
        if value_utc <= now:
            raise ValidationError('Due date must be in the future')
class UpdateTaskSchema(Schema):
    """Schema for updating a task"""
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(validate=validate.Length(max=1000))
    category = fields.String(validate=validate.Length(max=50))
    priority = fields.Integer(validate=validate.Range(min=1, max=5))
    impact = fields.Integer(validate=validate.Range(min=1, max=10))
    status = fields.String(validate=validate.OneOf(['pending', 'in-progress', 'completed', 'blocked']))
    progress = fields.Integer(validate=validate.Range(min=0, max=100))
    due_date = fields.DateTime()
    tags = fields.List(fields.String())
    complexity = fields.Integer(validate=validate.Range(min=1, max=5))
    estimated_hours = fields.Float(validate=validate.Range(min=0.1, max=1000))

    class Meta:
        unknown = EXCLUDE


class TaskStatusSchema(Schema):
    """Schema for updating task status"""
    status = fields.String(required=True, validate=validate.OneOf(['pending', 'in-progress', 'completed', 'blocked']))


class TaskProgressSchema(Schema):
    """Schema for updating task progress"""
    progress = fields.Integer(required=True, validate=validate.Range(min=0, max=100))


class BulkTaskSchema(Schema):
    """Schema for bulk task operations"""
    tasks = fields.List(fields.Dict(), required=True)

    class Meta:
        unknown = EXCLUDE


# Export all schemas
__all__ = [
    'RegisterSchema',
    'LoginSchema',
    'UpdateProfileSchema',
    'UpdatePreferencesSchema',
    'PasswordResetSchema',
    'CreateTaskSchema',
    'UpdateTaskSchema',
    'TaskStatusSchema',
    'TaskProgressSchema',
    'BulkTaskSchema'
]