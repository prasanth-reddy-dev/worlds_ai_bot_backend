"""
Input validation utilities for backend routes
"""
import re
from functools import wraps
from flask import request, jsonify

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (6-15 digits, can include + for country code)"""
    # Remove + and spaces for validation
    cleaned = str(phone).replace('+', '').replace(' ', '').replace('-', '')
    # Must be 6-15 digits
    return len(cleaned) >= 6 and len(cleaned) <= 15 and cleaned.isdigit()

def validate_password(password):
    """Validate password strength (min 6 chars)"""
    return len(password) >= 6

def validate_required_fields(data, required_fields):
    """Check if all required fields are present and not empty"""
    if not data:
        return False, "Request body is required"
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"
    
    return True, None

def require_fields(*fields):
    """Decorator to validate required fields in request body"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            
            is_valid, error_message = validate_required_fields(data, fields)
            if not is_valid:
                return jsonify({"message": error_message}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_string(text):
    """Remove potentially dangerous characters from strings"""
    if not isinstance(text, str):
        return text
    # Remove script tags and other dangerous content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # Remove all HTML tags
    return text.strip()

def sanitize_input(data):
    """Sanitize all string values in a dictionary"""
    if isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    return data
