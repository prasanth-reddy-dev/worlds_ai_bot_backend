from flask import Blueprint, request, jsonify
from config.database import mongo
from models.interview_questions_model import InterviewQuestions
from middlewares.auth import user_auth, admin_auth

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/create-interview', methods=['POST'])
@user_auth
@admin_auth
def create_interview():
    try:
        data = request.get_json()
        
        required_fields = ['topic', 'questions']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "Topic and questions are required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        new_interview = interview_model.create_interview_question(
            topic=data['topic'],
            questions=data['questions']
        )
        
        return jsonify({"message": "Interview question created successfully!", "interview": new_interview}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@interview_bp.route('/create-questions', methods=['POST'])
@user_auth
@admin_auth
def create_questions():
    """Endpoint to match frontend call - creates interview questions with topic and questions array"""
    try:
        data = request.get_json()
        
        required_fields = ['topic', 'questions']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "Topic and questions are required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        new_interview = interview_model.create_interview_question(
            topic=data['topic'],
            questions=data['questions']
        )
        
        return jsonify({"message": "Interview questions created successfully!", "interview": new_interview}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@interview_bp.route('/all-interviews', methods=['GET'])
def all_interviews():
    try:
        interview_model = InterviewQuestions(mongo)
        interviews = interview_model.find_all()
        return jsonify({"message": "Interview questions fetched successfully", "data": interviews if interviews else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoints to match frontend expectations
@interview_bp.route('/all-questions', methods=['GET'])
def all_questions():
    """Endpoint to match frontend call"""
    try:
        interview_model = InterviewQuestions(mongo)
        interviews = interview_model.find_all()
        return jsonify({"message": "Questions fetched successfully", "data": interviews if interviews else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@interview_bp.route('/delete-questions/<interview_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_questions(interview_id):
    """Delete interview question by ID - alternate endpoint"""
    try:
        if not interview_id:
            return jsonify({"message": "ID is required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        success = interview_model.delete_by_id(interview_id)
        
        if success:
            return jsonify({"message": "Interview question deleted successfully"}), 200
        else:
            return jsonify({"message": "Interview question not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@interview_bp.route('/show-interview/<interview_id>', methods=['GET'])
def show_interview(interview_id):
    try:
        interview_model = InterviewQuestions(mongo)
        interview = interview_model.find_by_id(interview_id)
        
        if not interview:
            return jsonify({"message": "Interview question not found"}), 404
        
        return jsonify(interview), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@interview_bp.route('/show-questions/<interview_id>', methods=['GET'])
def show_questions(interview_id):
    """Endpoint to match frontend call - retrieves interview questions by ID"""
    try:
        interview_model = InterviewQuestions(mongo)
        interview = interview_model.find_by_id(interview_id)
        
        if not interview:
            return jsonify({"message": "Questions not found"}), 404
        
        return jsonify(interview), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@interview_bp.route('/update-interview/<interview_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_interview(interview_id):
    try:
        data = request.get_json()
        
        if not interview_id:
            return jsonify({"message": "ID is required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        success = interview_model.update_by_id(
            interview_id=interview_id,
            topic=data.get('topic'),
            questions=data.get('questions')
        )
        
        if success:
            return jsonify({"message": "Interview question updated successfully"}), 200
        else:
            return jsonify({"message": "Interview question not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@interview_bp.route('/update-questions/<interview_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_questions(interview_id):
    """Endpoint to match frontend call - updates interview questions with topic and questions array"""
    try:
        data = request.get_json()
        
        if not interview_id:
            return jsonify({"message": "ID is required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        success = interview_model.update_by_id(
            interview_id=interview_id,
            topic=data.get('topic'),
            questions=data.get('questions')
        )
        
        if success:
            return jsonify({"message": "Questions updated successfully"}), 200
        else:
            return jsonify({"message": "Questions not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@interview_bp.route('/delete-interview/<interview_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_interview(interview_id):
    try:
        if not interview_id:
            return jsonify({"message": "ID is required"}), 422
        
        interview_model = InterviewQuestions(mongo)
        success = interview_model.delete_by_id(interview_id)
        
        if success:
            return jsonify({"message": "Interview question deleted successfully"}), 200
        else:
            return jsonify({"message": "Interview question not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
