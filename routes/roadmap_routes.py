from flask import Blueprint, request, jsonify
from config.database import mongo
from models.roadmap_model import RoadMap
from middlewares.auth import user_auth, admin_auth
from utils.validation import sanitize_input

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/create-roadmap', methods=['POST'])
@user_auth
@admin_auth
def create_roadmap():
    try:
        data = request.get_json()
        
        required_fields = ['courseName', 'tutorName', 'tutorDescription', 'tutorImageUrl', 'skills']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required"}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        roadmap_model = RoadMap(mongo)
        new_roadmap = roadmap_model.create_roadmap(
            course_name=data['courseName'],
            tutor_name=data['tutorName'],
            tutor_description=data['tutorDescription'],
            tutor_image_url=data['tutorImageUrl'],
            skills=data['skills']
        )
        
        return jsonify({"message": "Roadmap created successfully"}), 201
    
    except Exception as e:
        print(f"Create roadmap error: {str(e)}")
        return jsonify({"message": "Failed to create roadmap"}), 500


@roadmap_bp.route('/show-roadmaps', methods=['GET'])
def show_roadmaps():
    try:
        roadmap_model = RoadMap(mongo)
        roadmaps = roadmap_model.find_all()
        # Return consistent format with data wrapper
        return jsonify({"message": "Roadmaps fetched successfully", "data": roadmaps if roadmaps else []}), 200
    except Exception as e:
        print(f"Show roadmaps error: {str(e)}")
        return jsonify({"message": "Error retrieving roadmaps"}), 500


@roadmap_bp.route('/show-roadmap/<roadmap_id>', methods=['GET'])
def show_roadmap(roadmap_id):
    try:
        roadmap_model = RoadMap(mongo)
        roadmap = roadmap_model.find_by_id(roadmap_id)
        if not roadmap:
            return jsonify({"message": "Roadmap not found"}), 404
        return jsonify(roadmap), 200
    except Exception as e:
        print(f"Show roadmap error: {str(e)}")
        return jsonify({"message": "Error retrieving roadmap"}), 500


@roadmap_bp.route('/update-roadmap/<roadmap_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_roadmap(roadmap_id):
    try:
        data = request.get_json()
        
        # Sanitize input
        data = sanitize_input(data)
        
        roadmap_model = RoadMap(mongo)
        success = roadmap_model.update_by_id(
            roadmap_id=roadmap_id,
            course_name=data.get('courseName'),
            tutor_name=data.get('tutorName'),
            tutor_description=data.get('tutorDescription'),
            tutor_image_url=data.get('tutorImageUrl'),
            skills=data.get('skills')
        )
        
        if success:
            return jsonify({"message": "Roadmap updated successfully"}), 200
        else:
            return jsonify({"message": "Roadmap not found"}), 404
    
    except Exception as e:
        print(f"Update roadmap error: {str(e)}")
        return jsonify({"message": "Failed to update roadmap"}), 500


@roadmap_bp.route('/delete-roadmap/<roadmap_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_roadmap(roadmap_id):
    try:
        roadmap_model = RoadMap(mongo)
        success = roadmap_model.delete_by_id(roadmap_id)
        
        if success:
            return jsonify({"message": "Roadmap deleted successfully"}), 200
        else:
            return jsonify({"message": "Roadmap not found"}), 404
    
    except Exception as e:
        print(f"Delete roadmap error: {str(e)}")
        return jsonify({"message": "Failed to delete roadmap"}), 500