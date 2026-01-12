from flask import Blueprint, request, jsonify
from config.database import mongo
from models.course_model import Course
from middlewares.auth import user_auth, admin_auth
from utils.validation import sanitize_input

course_bp = Blueprint('course', __name__)

@course_bp.route('/create-course', methods=['POST'])
@user_auth
@admin_auth
def create_course():
    try:
        data = request.get_json()
        
        required_fields = ['courseName', 'imageUrl', 'price', 'duration', 'enrolled', 'status', 'badge', 'hours', 'nextId', 'recordingId']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required"}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        course_model = Course(mongo)
        new_course = course_model.create_course(
            course_name=data['courseName'],
            image_url=data['imageUrl'],
            price=data['price'],
            duration=data['duration'],
            enrolled=data['enrolled'],
            status=data['status'],
            badge=data['badge'],
            hours=data['hours'],
            next_id=data['nextId'],
            recording_id=data['recordingId'],
            coupon=data.get('coupon')  # Optional field
        )
        
        return jsonify({"message": "Course created successfully"}), 201
    
    except Exception as e:
        print(f"Create course error: {str(e)}")
        return jsonify({"message": "Failed to create course"}), 500


@course_bp.route('/show-course/<course_id>', methods=['GET'])
def show_course(course_id):
    try:
        course_model = Course(mongo)
        course = course_model.find_by_id(course_id)
        
        if not course:
            return jsonify({"message": "Course not found"}), 404
        
        return jsonify(course), 200
    except Exception as e:
        print(f"Show course error: {str(e)}")
        return jsonify({"message": "Error retrieving course"}), 500


@course_bp.route('/show-courses', methods=['GET'])
def show_courses():
    try:
        course_model = Course(mongo)
        courses = course_model.find_all()
        return jsonify({"message": "Courses fetched successfully", "data": courses}), 200
    except Exception as e:
        print(f"Show courses error: {str(e)}")
        return jsonify({"message": "Failed to fetch courses"}), 500


@course_bp.route('/update-course/<course_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_course(course_id):
    try:
        data = request.get_json()
        
        required_fields = ['courseName', 'imageUrl', 'price', 'status', 'enrolled', 'badge', 'hours', 'nextId', 'recordingId']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required"}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        course_model = Course(mongo)
        success = course_model.update_by_id(
            course_id=course_id,
            courseName=data.get('courseName'),
            imageUrl=data.get('imageUrl'),
            price=data.get('price'),
            duration=data.get('duration'),
            enrolled=data.get('enrolled'),
            status=data.get('status'),
            badge=data.get('badge'),
            hours=data.get('hours'),
            nextId=data.get('nextId'),
            recordingId=data.get('recordingId'),
            coupon=data.get('coupon').upper() if data.get('coupon') else None  # Convert to uppercase
        )
        
        if success:
            return jsonify({"message": "Course updated successfully"}), 200
        else:
            return jsonify({"message": "Course not found"}), 404
    
    except Exception as e:
        print(f"Update course error: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500


@course_bp.route('/validate-coupon/<course_id>', methods=['POST'])
def validate_coupon(course_id):
    """Validate coupon code for a course (case-insensitive)"""
    try:
        data = request.get_json()
        provided_coupon = data.get('coupon', '').strip().upper()  # Convert to uppercase
        
        if not provided_coupon:
            return jsonify({"valid": False, "message": "Coupon code is required"}), 400
        
        course_model = Course(mongo)
        course = course_model.find_by_id(course_id)
        
        if not course:
            return jsonify({"valid": False, "message": "Course not found"}), 404
        
        course_coupon = course.get('coupon')
        
        # If course has no coupon, invalid
        if not course_coupon:
            return jsonify({"valid": False, "message": "This course does not accept coupons"}), 400
        
        # Case-insensitive comparison (both are uppercase now)
        if provided_coupon == course_coupon:
            return jsonify({"valid": True, "message": "Coupon is valid! Course is FREE"}), 200
        else:
            return jsonify({"valid": False, "message": "Invalid coupon code"}), 400
    
    except Exception as e:
        print(f"Validate coupon error: {str(e)}")
        return jsonify({"valid": False, "message": "Internal server error"}), 500


@course_bp.route('/delete-course/<course_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_course(course_id):
    try:
        course_model = Course(mongo)
        success = course_model.delete_by_id(course_id)
        
        if success:
            return jsonify({"message": "Course deleted"}), 200
        else:
            return jsonify({"message": "Course not found"}), 404
    
    except Exception as e:
        print(f"Delete course error: {str(e)}")
        return jsonify({"message": "Failed to delete course"}), 500