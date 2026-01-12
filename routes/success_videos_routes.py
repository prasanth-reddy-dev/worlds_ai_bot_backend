from flask import Blueprint, request, jsonify
from config.database import mongo
from models.success_videos_model import SuccessVideos
from middlewares.auth import user_auth, admin_auth

success_videos_bp = Blueprint('success_videos', __name__)

@success_videos_bp.route('/create-video', methods=['POST'])
@user_auth
@admin_auth
def create_video():
    try:
        data = request.get_json()
        
        required_fields = ['videoUrl', 'jobRole', 'name', 'package', 'companyName']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required: videoUrl, jobRole, name, package, companyName"}), 422
        
        video_model = SuccessVideos(mongo)
        new_video = video_model.create_success_video(
            video_url=data['videoUrl'],
            job_role=data['jobRole'],
            name=data['name'],
            package=data['package'],
            company_name=data['companyName']
        )
        
        return jsonify({"message": "Video created successfully!", "video": new_video}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@success_videos_bp.route('/all-videos', methods=['GET'])
def all_videos():
    try:
        video_model = SuccessVideos(mongo)
        videos = video_model.find_all()
        return jsonify({"message": "Videos fetched successfully", "data": videos if videos else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend expectations
@success_videos_bp.route('/show-videos', methods=['GET'])
def show_videos():
    """Endpoint to match frontend call"""
    try:
        video_model = SuccessVideos(mongo)
        videos = video_model.find_all()
        return jsonify({"message": "Videos fetched successfully", "data": videos if videos else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@success_videos_bp.route('/show-video/<video_id>', methods=['GET'])
def show_video(video_id):
    try:
        video_model = SuccessVideos(mongo)
        video = video_model.find_by_id(video_id)
        
        if not video:
            return jsonify({"message": "Video not found"}), 404
        
        return jsonify(video), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@success_videos_bp.route('/update-video/<video_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_video(video_id):
    try:
        data = request.get_json()
        
        if not video_id:
            return jsonify({"message": "ID is required"}), 422
        
        video_model = SuccessVideos(mongo)
        success = video_model.update_by_id(
            video_id=video_id,
            video_url=data.get('videoUrl'),
            job_role=data.get('jobRole'),
            name=data.get('name'),
            package=data.get('package'),
            company_name=data.get('companyName')
        )
        
        if success:
            return jsonify({"message": "Video updated successfully"}), 200
        else:
            return jsonify({"message": "Video not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@success_videos_bp.route('/delete-video/<video_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_video(video_id):
    try:
        if not video_id:
            return jsonify({"message": "ID is required"}), 422
        
        video_model = SuccessVideos(mongo)
        success = video_model.delete_by_id(video_id)
        
        if success:
            return jsonify({"message": "Video deleted successfully"}), 200
        else:
            return jsonify({"message": "Video not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
