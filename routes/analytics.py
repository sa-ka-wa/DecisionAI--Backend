from flask import Blueprint, request, jsonify
from controllers.analytics_controller import (
    get_dashboard_stats, get_completion_rate,
    get_category_breakdown, get_impact_analysis,
    get_priority_distribution, get_timeline_data,
    get_performance_metrics, get_productivity_score,
    get_ai_recommendations, get_optimization_tips,
    get_risk_analysis, export_analytics_data
)
from middleware.auth_middleware import jwt_required

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard_stats():
    """Get dashboard statistics"""
    return get_dashboard_stats(request.user)

@analytics_bp.route('/completion-rate', methods=['GET'])
@jwt_required
def completion_rate():
    """Get completion rate over time"""
    period = request.args.get('period', 'week')
    return get_completion_rate(request.user, period)

@analytics_bp.route('/category-breakdown', methods=['GET'])
@jwt_required
def category_breakdown():
    """Get category breakdown"""
    return get_category_breakdown(request.user)

@analytics_bp.route('/impact-analysis', methods=['GET'])
@jwt_required
def impact_analysis():
    """Get impact analysis"""
    return get_impact_analysis(request.user)

@analytics_bp.route('/priority-distribution', methods=['GET'])
@jwt_required
def priority_distribution():
    """Get priority distribution"""
    return get_priority_distribution(request.user)

@analytics_bp.route('/timeline', methods=['GET'])
@jwt_required
def timeline():
    """Get timeline data"""
    return get_timeline_data(request.user)

@analytics_bp.route('/performance', methods=['GET'])
@jwt_required
def performance():
    """Get performance metrics"""
    return get_performance_metrics(request.user)

@analytics_bp.route('/productivity', methods=['GET'])
@jwt_required
def productivity():
    """Get productivity score"""
    return get_productivity_score(request.user)

@analytics_bp.route('/ai/recommendations', methods=['GET'])
@jwt_required
def ai_recommendations():
    """Get AI recommendations"""
    return get_ai_recommendations(request.user)

@analytics_bp.route('/ai/optimization', methods=['GET'])
@jwt_required
def optimization_tips():
    """Get optimization tips"""
    return get_optimization_tips(request.user)

@analytics_bp.route('/ai/risk-analysis', methods=['GET'])
@jwt_required
def risk_analysis():
    """Get risk analysis"""
    return get_risk_analysis(request.user)

@analytics_bp.route('/export', methods=['GET'])
@jwt_required
def export():
    """Export analytics data"""
    format_type = request.args.get('format', 'json')
    return export_analytics_data(request.user, format_type)