from flask import Blueprint, request, jsonify
from config.database import mongo
from models.user_model import User
from middlewares.auth import user_auth, admin_auth
from utils.validation import sanitize_input

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@user_auth
def profile():
    try:
        user = request.current_user
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        print(f"Profile error: {str(e)}")
        return jsonify({"message": "Error fetching profile"}), 500


@profile_bp.route('/all-users', methods=['GET'])
@user_auth
@admin_auth
def all_users():
    try:
        user_model = User(mongo)
        users = user_model.find_all()
        return jsonify(users), 200
    except Exception as e:
        print(f"All users error: {str(e)}")
        return jsonify({"message": "Error fetching users"}), 500


@profile_bp.route('/show-profiles', methods=['GET'])
@user_auth
def show_profiles():
    """Endpoint to match frontend call"""
    try:
        if request.current_user.get('role') != 'admin':
            return jsonify({"message": "Access denied. Admin only."}), 403
        
        user_model = User(mongo)
        users = user_model.find_all()
        return jsonify({"data": users}), 200
    except Exception as e:
        print(f"Show profiles error: {str(e)}")
        return jsonify({"message": "Error fetching user profiles"}), 500


@profile_bp.route('/delete-profile/<user_id>', methods=['DELETE'])
@user_auth
def delete_profile(user_id):
    """Delete user by ID"""
    try:
        if request.current_user.get('role') != 'admin':
            return jsonify({"message": "Access denied. Admin only."}), 403
        
        user_model = User(mongo)
        success = user_model.delete_by_id(user_id)
        
        if success:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Delete profile error: {str(e)}")
        return jsonify({"message": "Failed to delete user"}), 500


@profile_bp.route('/profile/edit', methods=['PATCH'])
@user_auth
def edit_profile():
    try:
        user_id = request.current_user_id
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        data = sanitize_input(data)
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'contact' in data:  # Changed from 'number' to 'contact'
            update_data['contact'] = data['contact']
        if 'university' in data:  # Changed from 'universityName'
            update_data['university'] = data['university']
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, update_data)
        
        if updated_user:
            return jsonify(updated_user), 200
        else:
            return jsonify({"message": "Failed to update profile"}), 500
    
    except Exception as e:
        import traceback
        print(f"Edit profile error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"message": f"Failed to update profile: {str(e)}"}), 500


@profile_bp.route('/profile/delete', methods=['DELETE'])
@user_auth
def delete_account():
    """Allow students to delete their own account"""
    try:
        user_id = request.current_user_id
        user_model = User(mongo)
        
        # Delete the user account
        result = user_model.delete_by_id(user_id)
        
        if result:
            return jsonify({"message": "Account deleted successfully"}), 200
        else:
            return jsonify({"message": "Failed to delete account"}), 500
    
    except Exception as e:
        print(f"Delete account error: {str(e)}")
        return jsonify({"message": "Failed to delete account"}), 500


@profile_bp.route('/show-user/<user_id>', methods=['GET'])
@user_auth
def show_user(user_id):
    try:
        user_model = User(mongo)
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        return jsonify(user), 200
    except Exception as e:
        print(f"Show user error: {str(e)}")
        return jsonify({"message": "Error retrieving User"}), 500


@profile_bp.route('/update-user/<user_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_user(user_id):
    """Update user by ID"""
    try:
        data = request.get_json()
        data = sanitize_input(data)
        
        update_data = {}
        allowed_fields = ['name', 'email', 'number', 'role', 'batchNumber', 'paymentStatus', 'university',
                         'pCertificates', 'iCertificates', 'cCertificates', 'courses', 'invoiceUrl']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return jsonify({"message": "No fields to update"}), 400
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, update_data)
        
        if updated_user:
            return jsonify({"message": "User updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Update user error: {str(e)}")
        return jsonify({"message": "Failed to update user"}), 500


# Certificate Update Endpoints

@profile_bp.route('/update-pc/<user_id>', methods=['PUT', 'PATCH'])
@user_auth
@admin_auth
def update_pc_certificate(user_id):
    """Update Programming Certificate URL"""
    try:
        data = request.get_json()
        
        if not data or 'pCertificates' not in data:
            return jsonify({"message": "pCertificates field is required"}), 400
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, {'pCertificates': data['pCertificates']})
        
        if updated_user:
            return jsonify({"message": "Programming certificate updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Update PC error: {str(e)}")
        return jsonify({"message": "Failed to update certificate"}), 500


@profile_bp.route('/update-ic/<user_id>', methods=['PUT', 'PATCH'])
@user_auth
@admin_auth
def update_ic_certificate(user_id):
    """Update Internship Certificate URL"""
    try:
        data = request.get_json()
        
        if not data or 'iCertificates' not in data:
            return jsonify({"message": "iCertificates field is required"}), 400
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, {'iCertificates': data['iCertificates']})
        
        if updated_user:
            return jsonify({"message": "Internship certificate updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Update IC error: {str(e)}")
        return jsonify({"message": "Failed to update certificate"}), 500


@profile_bp.route('/update-cc/<user_id>', methods=['PUT', 'PATCH'])
@user_auth
@admin_auth
def update_cc_certificate(user_id):
    """Update Completion Certificate URL"""
    try:
        data = request.get_json()
        
        if not data or 'cCertificates' not in data:
            return jsonify({"message": "cCertificates field is required"}), 400
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, {'cCertificates': data['cCertificates']})
        
        if updated_user:
            return jsonify({"message": "Completion certificate updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Update CC error: {str(e)}")
        return jsonify({"message": "Failed to update certificate"}), 500


@profile_bp.route('/update-invoice/<user_id>', methods=['PUT', 'PATCH'])
@user_auth
@admin_auth
def update_invoice(user_id):
    """Update Invoice URL"""
    try:
        data = request.get_json()
        
        if not data or 'invoiceUrl' not in data:
            return jsonify({"message": "invoiceUrl field is required"}), 400
        
        user_model = User(mongo)
        updated_user = user_model.update_user(user_id, {'invoiceUrl': data['invoiceUrl']})
        
        if updated_user:
            return jsonify({"message": "Invoice updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e:
        print(f"Update invoice error: {str(e)}")
        return jsonify({"message": "Failed to update invoice"}), 500


@profile_bp.route('/payment-success', methods=['POST'])
@user_auth
def payment_success():
    """Add course to user after successful payment (for students)"""
    try:
        user = request.current_user
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        data = request.get_json()
        data = sanitize_input(data)
        
        # Extract payment data
        course_data = {
            'transactionId': data.get('transactionId') or data.get('paymentId'),  # Support both fields
            'amount': data.get('amount'),
            'status': True,
            'email': user.get('email'),
            'name': user.get('name'),
            'courseName': data.get('courseName'),
            'recordingsId': data.get('recordingsId') or data.get('recordingId'),  # Support both field names
            'courseId': data.get('courseId'),
            'purchaseDate': data.get('purchaseDate'),
            'recordingAccess': data.get('recordingAccess', True)  # Use provided value or default to True
        }
        
        # Get existing courses or initialize empty array
        user_model = User(mongo)
        user_data = user_model.find_by_id(user.get('_id'))
        existing_courses = user_data.get('courses', []) if user_data else []
        
        # Add new course
        existing_courses.append(course_data)
        
        # Update user with new course
        updated_user = user_model.update_user(user.get('_id'), {'courses': existing_courses})
        
        if updated_user:
            return jsonify({
                "message": "Course added successfully", 
                "user": updated_user,
                "course": course_data
            }), 200
        else:
            return jsonify({"message": "Failed to add course"}), 500
    
    except Exception as e:
        print(f"Payment success error: {str(e)}")
        return jsonify({"message": "Failed to process payment"}), 500
