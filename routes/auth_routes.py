from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity
from config.database import mongo
from models.user_model import User
from utils.email_service import EmailService
from utils.validation import validate_email, validate_phone, validate_password, sanitize_input
from middlewares.auth import user_auth
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('name', 'email', 'number', 'password')):
            return jsonify({"message": "All fields are required"}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        name = data['name']
        email = data['email']
        number = data['number']
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            return jsonify({"message": "Invalid email format"}), 400
        
        # Validate phone number
        if not validate_phone(number):
            return jsonify({"message": "Invalid phone number"}), 400
        
        # Validate password strength
        if not validate_password(password):
            return jsonify({"message": "Password must be at least 6 characters"}), 400
        
        # Check if user already exists
        user_model = User(mongo)
        existing_user = user_model.find_by_email(email)
        if existing_user:
            return jsonify({"message": "Email already exists"}), 400
        
        # Create new user
        new_user = user_model.create_user(name, email, number, password)
        
        # Send welcome email
        try:
            email_service = EmailService()
            email_service.send_welcome_email(email, name)
        except Exception as email_error:
            # Log email error but don't fail signup
            print(f"Email sending failed: {str(email_error)}")
        
        return jsonify({"message": "User created successfully", "user": new_user}), 200
    
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({"message": "An error occurred during signup"}), 500




@auth_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({"message": "Email and password are required"}), 400
        
        email = data['email']
        password = data['password']
        
        user_model = User(mongo)
        user = user_model.find_by_email(email)
        
        if not user:
            return jsonify({"message": "Invalid credentials"}), 401
        
        # Verify password
        if not user_model.verify_password(user['password'], password):
            return jsonify({"message": "Invalid credentials"}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        # Return response with token in Authorization header
        response = jsonify({"message": "Login successful", "user": user, "token": access_token})
        response.headers['Authorization'] = f'Bearer {access_token}'
        response.set_cookie('token', access_token, httponly=True, secure=True, samesite='None')
        
        return response, 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"message": "OK"})
        return response, 200
    
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route('/signout', methods=['POST', 'OPTIONS'])
def signout():
    """Alias for logout to match frontend expectations"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"message": "OK"})
        return response, 200
    
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"message": "Email is required"}), 400
        
        email = data['email']
        
        user_model = User(mongo)
        user = user_model.find_by_email(email)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # Generate reset token and expiry
        import jwt
        import time
        reset_token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': time.time() + 3600  # 1 hour expiry
        }, 'reset_secret_key', algorithm='HS256')
        
        # Update user with reset token
        user_model.update_field(str(user['_id']), 'resetToken', reset_token)
        user_model.update_field(str(user['_id']), 'resetTokenExpiry', time.time() + 3600)
        
        # Send reset email
        email_service = EmailService()
        import os
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"
        email_service.send_password_reset_email(email, reset_link)
        
        return jsonify({"message": "Password reset email sent"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('token', 'new_password')):
            return jsonify({"message": "Token and new password are required"}), 400
        
        token = data['token']
        new_password = data['new_password']
        
        try:
            import jwt
            import time
            decoded = jwt.decode(token, 'reset_secret_key', algorithms=['HS256'])
            user_id = decoded['user_id']
            
            # Check if token is still valid
            user_model = User(mongo)
            user = user_model.find_by_id(user_id)
            if not user or not user.get('resetToken') or user.get('resetTokenExpiry', 0) < time.time():
                return jsonify({"message": "Invalid or expired token"}), 400
            
            # Update password
            if user_model.update_password(user_id, new_password):
                # Clear reset token
                user_model.update_field(user_id, 'resetToken', None)
                user_model.update_field(user_id, 'resetTokenExpiry', None)
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                return jsonify({"message": "Failed to update password"}), 500
                
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 400
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500