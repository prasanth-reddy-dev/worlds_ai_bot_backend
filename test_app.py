"""
Test script to verify the Flask application can be imported and run without errors.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        print("Testing imports...")
        
        # Test main app import
        from app import create_app
        print("✓ Successfully imported create_app from app")
        
        # Test config import
        from config.config import Config
        print("✓ Successfully imported Config from config.config")
        
        # Test database import
        from config.database import init_db, mongo
        print("✓ Successfully imported database components")
        
        # Test model imports
        from models.user_model import User
        from models.course_model import Course
        from models.bootcamp_model import Bootcamp
        from models.roadmap_model import RoadMap
        from models.recording_model import Recording
        from models.contact_model import Contact
        from models.privacy_model import Privacy
        from models.register_model import Register
        from models.test_model import Test
        from models.job_model import Job
        from models.roadmap_topic_model import RoadMapTopic
        print("✓ Successfully imported all models")
        
        # Test route imports
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
        print("✓ Successfully imported all route blueprints")
        
        # Test middleware imports
        from middlewares.auth import user_auth, admin_auth, payment_auth
        print("✓ Successfully imported authentication middlewares")
        
        # Test utility imports
        from utils.email_service import EmailService
        print("✓ Successfully imported EmailService")
        
        print("\nAll imports successful! Flask app structure is valid.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created without errors"""
    try:
        print("\nTesting app creation...")
        from app import create_app
        
        app = create_app()
        print("✓ Successfully created Flask app instance")
        
        # Check if routes are registered
        print(f"✓ App has {len(app.url_map._rules)} routes registered")
        
        return True
    except Exception as e:
        print(f"✗ Error creating app: {e}")
        return False

if __name__ == "__main__":
    print("Starting Flask app tests...\n")
    
    imports_ok = test_imports()
    app_creation_ok = test_app_creation()
    
    if imports_ok and app_creation_ok:
        print("\n🎉 All tests passed! The Flask backend is ready.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)