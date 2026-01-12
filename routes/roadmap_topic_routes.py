from flask import Blueprint, request, jsonify
from config.database import mongo
from models.roadmap_topic_model import RoadMapTopic
from middlewares.auth import user_auth, admin_auth

roadmap_topic_bp = Blueprint('roadmap_topic', __name__)

@roadmap_topic_bp.route('/create-roadmap-topic', methods=['POST'])
@user_auth
@admin_auth
def create_roadmap_topic():
    try:
        data = request.get_json()
        
        required_fields = ['roadMapName', 'id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required..."}), 422
        
        roadmap_topic_model = RoadMapTopic(mongo)
        new_topic = roadmap_topic_model.create_roadmap_topic(
            road_map_name=data['roadMapName'],
            id=data['id']
        )
        
        return jsonify({"message": "Roadmap topic created successfully!!"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@roadmap_topic_bp.route('/show-roadmap-topic', methods=['GET'])
def show_roadmap_topics():
    try:
        roadmap_topic_model = RoadMapTopic(mongo)
        topics = roadmap_topic_model.find_all()
        return jsonify({"message": "Roadmap topics fetched successfully", "data": topics if topics else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@roadmap_topic_bp.route('/show-roadmap-topic/<topic_id>', methods=['GET'])
def show_roadmap_topic(topic_id):
    try:
        roadmap_topic_model = RoadMapTopic(mongo)
        topic = roadmap_topic_model.find_by_id(topic_id)
        
        if not topic:
            return jsonify({"message": "Roadmap topic not found"}), 404
        
        return jsonify(topic), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@roadmap_topic_bp.route('/update-roadmap-topic/<topic_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_roadmap_topic(topic_id):
    try:
        data = request.get_json()
        
        if not topic_id:
            return jsonify({"message": "ID is required"}), 422
        
        roadmap_topic_model = RoadMapTopic(mongo)
        success = roadmap_topic_model.update_by_id(
            roadmap_topic_id=topic_id,
            road_map_name=data.get('roadMapName'),
            id=data.get('id')
        )
        
        if success:
            return jsonify({"message": "Roadmap topic updated successfully"}), 200
        else:
            return jsonify({"message": "Roadmap topic not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@roadmap_topic_bp.route('/delete-roadmap-topic/<topic_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_roadmap_topic(topic_id):
    try:
        if not topic_id:
            return jsonify({"message": "ID is required"}), 422
        
        roadmap_topic_model = RoadMapTopic(mongo)
        success = roadmap_topic_model.delete_by_id(topic_id)
        
        if success:
            return jsonify({"message": "Roadmap topic deleted successfully"}), 200
        else:
            return jsonify({"message": "Roadmap topic not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500