from flask import Blueprint, request, jsonify
from config.database import mongo
from models.feedback_model import Feedback
from middlewares.auth import user_auth, admin_auth

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/create-feedback', methods=['POST'])
def create_feedback():
    """Create new feedback from contact form - no auth required"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'message']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "Name, email and message are required"}), 422
        
        feedback_model = Feedback(mongo)
        new_feedback = feedback_model.create_feedback(
            name=data['name'],
            email=data['email'],
            mobile=data.get('mobile', ''),
            message=data['message']
        )
        
        return jsonify({"message": "Thank you for your feedback!", "feedback": new_feedback}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@feedback_bp.route('/all-feedbacks', methods=['GET'])
@user_auth
@admin_auth
def all_feedbacks():
    """Get all feedbacks - admin only"""
    try:
        feedback_model = Feedback(mongo)
        feedbacks = feedback_model.find_all()
        return jsonify({"message": "Feedbacks fetched successfully", "data": feedbacks if feedbacks else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@feedback_bp.route('/show-feedback/<feedback_id>', methods=['GET'])
@user_auth
@admin_auth
def show_feedback(feedback_id):
    """Get single feedback - admin only"""
    try:
        feedback_model = Feedback(mongo)
        feedback = feedback_model.find_by_id(feedback_id)
        
        if not feedback:
            return jsonify({"message": "Feedback not found"}), 404
        
        return jsonify(feedback), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@feedback_bp.route('/update-feedback/<feedback_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_feedback(feedback_id):
    """Update feedback status - admin only"""
    try:
        data = request.get_json()
        
        if not feedback_id:
            return jsonify({"message": "ID is required"}), 422
        
        feedback_model = Feedback(mongo)
        status = data.get('status', 'pending')
        success = feedback_model.update_status(feedback_id, status)
        
        if success:
            return jsonify({"message": "Feedback updated successfully"}), 200
        else:
            return jsonify({"message": "Feedback not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@feedback_bp.route('/delete-feedback/<feedback_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_feedback(feedback_id):
    """Delete feedback - admin only"""
    try:
        if not feedback_id:
            return jsonify({"message": "ID is required"}), 422
        
        feedback_model = Feedback(mongo)
        success = feedback_model.delete_by_id(feedback_id)
        
        if success:
            return jsonify({"message": "Feedback deleted successfully"}), 200
        else:
            return jsonify({"message": "Feedback not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
