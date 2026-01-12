from flask import Blueprint, request, jsonify
from config.database import mongo
from models.recording_model import Recording
from middlewares.auth import user_auth, admin_auth, payment_auth

recording_bp = Blueprint('recording', __name__)

@recording_bp.route('/create-recordings', methods=['POST'])
@user_auth
@admin_auth
def create_recordings():
    try:
        data = request.get_json()
        
        required_fields = ['batchNumber', 'recordings']
        if not data or not all(field in data for field in required_fields) or not data['recordings'] or len(data['recordings']) == 0:
            return jsonify({"message": "Please fill all the fields"}), 422
        
        recording_model = Recording(mongo)
        new_recording = recording_model.create_recording(
            batch_number=data['batchNumber'],
            recordings=data['recordings'],
            status=data.get('status', True)  # Default to active
        )
        
        return jsonify({"message": "Recording added successfully"}), 200
    
    except Exception as e:
        return jsonify({"message": "Something went wrong", "error": str(e)}), 500


@recording_bp.route('/show-recordings', methods=['GET'])
@user_auth
@admin_auth
def show_recordings():
    try:
        recording_model = Recording(mongo)
        recordings = recording_model.find_all()
        
        if not recordings:
            return jsonify({"data": []}), 200
        
        return jsonify({"data": recordings}), 200
    
    except Exception as e:
        return jsonify({"message": "Something went wrong", "error": str(e)}), 500


@recording_bp.route('/show-recording/<recording_id>', methods=['GET'])
@recording_bp.route('/show-recordings/<recording_id>', methods=['GET'])
@user_auth  # Only require user authentication, not admin
def show_recording(recording_id):
    try:
        recording_model = Recording(mongo)
        recording = recording_model.find_by_id(recording_id)
        
        if not recording:
            return jsonify({"message": "Recording not found"}), 404
        
        return jsonify(recording), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@recording_bp.route('/update-recordings/<recording_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_recordings(recording_id):
    try:
        data = request.get_json()
        
        if not recording_id:
            return jsonify({"message": "ID is required"}), 422
        
        recording_model = Recording(mongo)
        success = recording_model.update_by_id(
            recording_id=recording_id,
            batch_number=data.get('batchNumber'),
            recordings=data.get('recordings'),
            status=data.get('status')  # Allow status toggle
        )
        
        if success:
            return jsonify({"message": "Recording updated successfully"}), 200
        else:
            return jsonify({"message": "Recording not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@recording_bp.route('/delete-recordings/<recording_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_recordings(recording_id):
    try:
        if not recording_id:
            return jsonify({"message": "ID is required"}), 422
        
        recording_model = Recording(mongo)
        success = recording_model.delete_by_id(recording_id)
        
        if success:
            return jsonify({"message": "Recording deleted successfully"}), 200
        else:
            return jsonify({"message": "Recording not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@recording_bp.route('/student-recording/<recording_id>', methods=['GET'])
@user_auth
def student_recording(recording_id):
    """Public endpoint for students to view recordings (checks status)"""
    try:
        recording_model = Recording(mongo)
        recording = recording_model.find_by_id(recording_id)
        
        if not recording:
            return jsonify({"message": "Recording not found", "access": False}), 404
        
        # Check if recording is active
        if not recording.get('status', False):
            return jsonify({
                "message": "This course is currently unavailable. Please contact support.",
                "access": False
            }), 403
        
        # Return recording data if active
        return jsonify({
            "data": recording,
            "access": True
        }), 200
        
    except Exception as e:
        return jsonify({"message": str(e), "access": False}), 500