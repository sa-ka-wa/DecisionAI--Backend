from flask import Flask, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from extensions import db, migrate, jwt, cors

def create_app():
    """Factory pattern for Flask app"""
    app = Flask(__name__)

    # --------------------------
    # Configuration
    # --------------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///decisionai.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-this-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['DEBUG'] = os.getenv('DEBUG', 'true').lower() == 'true'
    app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    app.config['API_PREFIX'] = os.getenv('API_PREFIX', '/api/v1')

    # --------------------------
    # Initialize extensions
    # --------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # --------------------------
    # Logging
    # --------------------------
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )

    # --------------------------
    # Blueprints / Routes
    # --------------------------
    try:
        from routes.auth import auth_bp
        from routes.tasks import tasks_bp
        from routes.analytics import analytics_bp

        api_prefix = app.config['API_PREFIX']
        app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
        app.register_blueprint(tasks_bp, url_prefix=f'{api_prefix}/tasks')
        app.register_blueprint(analytics_bp, url_prefix=f'{api_prefix}/analytics')


        print("✅ Blueprints registered successfully")

    except ImportError as e:
        print(f"Warning: Could not import blueprints: {e}")
        print("Using fallback test routes...")

        @app.route('/test')
        def test():
            return jsonify({'message': 'API is working (fallback)'})

    # --------------------------
    # Health check
    # --------------------------
    @app.route('/health')
    def health_check():
        from datetime import datetime
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    # --------------------------
    # Database initialization
    # --------------------------
    with app.app_context():
        db.create_all()

    # --------------------------
    # Error handlers
    # --------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    return app

# --------------------------
# Create app instance
# --------------------------
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
