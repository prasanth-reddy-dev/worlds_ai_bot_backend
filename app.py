from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config
from config.database import init_db, mongo
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.course_routes import course_bp
from routes.bootcamp_routes import bootcamp_bp
from routes.roadmap_routes import roadmap_bp
from routes.recording_routes import recording_bp
from routes.contact_routes import contact_bp
from routes.privacy_routes import privacy_bp
from routes.register_routes import register_bp
from routes.test_routes import test_bp
from routes.job_routes import job_bp
from routes.roadmap_topic_routes import roadmap_topic_bp
from routes.interview_questions_routes import interview_bp
from routes.success_videos_routes import success_videos_bp
from routes.company_logos_routes import company_logos_bp
from routes.feedback_routes import feedback_bp
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Set JWT expiration to 24 hours
    from datetime import timedelta
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Configure JWT to accept tokens from headers and cookies
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Production-ready JWT cookie settings
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.config['JWT_COOKIE_SECURE'] = is_production  # True in production (HTTPS)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF for now
    app.config['JWT_COOKIE_SAMESITE'] = 'None' if is_production else 'Lax'
    
    # Initialize extensions
    init_db(app)
    jwt = JWTManager(app)
    
    # Configure CORS with enhanced options
    allowed_origins = [
        Config.FRONTEND_URL,
        'https://worldsaibot.com',
        'https://www.worldsaibot.com',
        'https://worlds-ai-bot-frontend.vercel.app',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:5174',
        'http://127.0.0.1:5174',
        'http://localhost:5175',
        'http://127.0.0.1:5175'
    ]
    
    # Add any Vercel preview URLs (they have random subdomains)
    cors_config = {
        'origins': '*',  # Allow all origins for now (can restrict later)
        'methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept'],
        'supports_credentials': True
    }
    
    CORS(app, resources={r"/*": cors_config})
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')
    app.register_blueprint(course_bp, url_prefix='/')
    app.register_blueprint(bootcamp_bp, url_prefix='/')
    app.register_blueprint(roadmap_bp, url_prefix='/')
    app.register_blueprint(recording_bp, url_prefix='/')
    app.register_blueprint(contact_bp, url_prefix='/')
    app.register_blueprint(privacy_bp, url_prefix='/')
    app.register_blueprint(register_bp, url_prefix='/')
    app.register_blueprint(test_bp, url_prefix='/')
    app.register_blueprint(job_bp, url_prefix='/')
    app.register_blueprint(roadmap_topic_bp, url_prefix='/')
    app.register_blueprint(interview_bp, url_prefix='/')
    app.register_blueprint(success_videos_bp, url_prefix='/')
    app.register_blueprint(company_logos_bp, url_prefix='/')
    app.register_blueprint(feedback_bp, url_prefix='/')
    
    # Root route
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Worlds AI Bot Flask Backend Running!"}), 200
    
    # Global error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Route not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)