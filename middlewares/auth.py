from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from config.database import mongo
from models.user_model import User

def user_auth(f):
    """Authentication middleware - checks if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token from either cookies or Authorization header
            verify_jwt_in_request()
            
            # Get user ID from token
            user_id = get_jwt_identity()
            
            # Get user from database
            user_model = User(mongo)
            user = user_model.find_by_id(user_id)
            
            if not user:
                return jsonify({"message": "User not found"}), 404
            
            # Add user to request context
            request.current_user = user
            request.current_user_id = user_id
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    
    return decorated_function


def admin_auth(f):
    """Authorization middleware - checks if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token first
            verify_jwt_in_request()
            
            # Get user ID from token
            user_id = get_jwt_identity()
            
            # Get user from database
            user_model = User(mongo)
            user = user_model.find_by_id(user_id)
            
            if not user:
                return jsonify({"message": "User not found"}), 404
            
            # Check if user role is admin
            if user.get("role") != "admin":
                return jsonify({"message": "Access denied. Admin only."}), 403
            
            # Add user to request context
            request.current_user = user
            request.current_user_id = user_id
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return decorated_function


def payment_auth(f):
    """Payment authorization middleware - checks if user has paid for courses"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token
            verify_jwt_in_request()
            
            # Get user ID from token
            user_id = get_jwt_identity()
            
            # Get user from database
            user_model = User(mongo)
            user = user_model.find_by_id(user_id)
            
            if not user:
                return jsonify({"message": "User not found"}), 404
            
            # Check if user has paid (courses array length > 0)
            courses = user.get("courses", [])
            if not courses or len(courses) < 1:
                return jsonify({"message": "Access denied. Payment required."}), 403
            
            # Add user to request context
            request.current_user = user
            request.current_user_id = user_id
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return decorated_function