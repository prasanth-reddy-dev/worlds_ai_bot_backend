from flask import Blueprint, request, jsonify
from config.database import mongo
from models.bootcamp_model import Bootcamp
from middlewares.auth import user_auth, admin_auth
from utils.validation import sanitize_input

bootcamp_bp = Blueprint('bootcamp', __name__)

@bootcamp_bp.route('/create-bootcamp', methods=['POST'])
@user_auth
@admin_auth
def create_bootcamp():
    try:
        data = request.get_json()
        
        required_fields = ['days', 'courseName', 'startDate', 'endDate', 'startTime', 'courseRoadmap', 'videoUrl', 'instructors']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required"}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        bootcamp_model = Bootcamp(mongo)
        new_bootcamp = bootcamp_model.create_bootcamp(
            days=data['days'],
            course_name=data['courseName'],
            start_date=data['startDate'],
            end_date=data['endDate'],
            start_time=data['startTime'],
            course_roadmap=data['courseRoadmap'],
            video_url=data['videoUrl'],
            instructors=data['instructors']
        )
        
        return jsonify({"message": "Bootcamp created successfully!", "bootcamp": new_bootcamp}), 201
    
    except Exception as e:
        print(f"Create bootcamp error: {str(e)}")
        return jsonify({"message": "Failed to create bootcamp"}), 500


@bootcamp_bp.route('/all-bootcamps', methods=['GET'])
def all_bootcamps():
    try:
        bootcamp_model = Bootcamp(mongo)
        bootcamps = bootcamp_model.find_all()
        return jsonify({"message": "Bootcamps fetched successfully", "data": bootcamps}), 200
    except Exception as e:
        print(f"All bootcamps error: {str(e)}")
        return jsonify({"message": "Failed to fetch bootcamps"}), 500


@bootcamp_bp.route('/show-bootcamp/<bootcamp_id>', methods=['GET'])
def show_bootcamp(bootcamp_id):
    try:
        bootcamp_model = Bootcamp(mongo)
        bootcamp = bootcamp_model.find_by_id(bootcamp_id)
        
        if not bootcamp:
            return jsonify({"message": "Bootcamp not found"}), 404
        
        return jsonify(bootcamp), 200
    except Exception as e:
        print(f"Show bootcamp error: {str(e)}")
        return jsonify({"message": "Error retrieving bootcamp"}), 500


@bootcamp_bp.route('/update-bootcamp/<bootcamp_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_bootcamp(bootcamp_id):
    try:
        data = request.get_json()
        
        # Sanitize input
        data = sanitize_input(data)
        
        bootcamp_model = Bootcamp(mongo)
        success = bootcamp_model.update_by_id(
            bootcamp_id,
            days=data.get('days'),
            course_name=data.get('courseName'),
            start_date=data.get('startDate'),
            end_date=data.get('endDate'),
            start_time=data.get('startTime'),
            course_roadmap=data.get('courseRoadmap'),
            video_url=data.get('videoUrl'),
            instructors=data.get('instructors')
        )
        
        if success:
            return jsonify({"message": "Bootcamp updated successfully"}), 200
        else:
            return jsonify({"message": "Bootcamp not found"}), 404
    
    except Exception as e:
        print(f"Update bootcamp error: {str(e)}")
        return jsonify({"message": "Failed to update bootcamp"}), 500


@bootcamp_bp.route('/delete-bootcamp/<bootcamp_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_bootcamp(bootcamp_id):
    try:
        bootcamp_model = Bootcamp(mongo)
        success = bootcamp_model.delete_by_id(bootcamp_id)
        
        if success:
            return jsonify({"message": "Bootcamp deleted successfully"}), 200
        else:
            return jsonify({"message": "Bootcamp not found"}), 404
    
    except Exception as e:
        print(f"Delete bootcamp error: {str(e)}")
        return jsonify({"message": "Failed to delete bootcamp"}), 500