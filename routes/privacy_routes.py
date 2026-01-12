from flask import Blueprint, request, jsonify
from config.database import mongo
from models.privacy_model import Privacy
from middlewares.auth import user_auth, admin_auth

privacy_bp = Blueprint('privacy', __name__)

@privacy_bp.route('/create-privacy', methods=['POST'])
@user_auth
@admin_auth
def create_privacy():
    try:
        data = request.get_json()
        
        if not data or not all(field in data for field in ['heading', 'paragraph']):
            return jsonify({"message": "Heading and paragraph are required."}), 422
        
        privacy_model = Privacy(mongo)
        new_privacy = privacy_model.create_privacy(
            heading=data['heading'],
            paragraph=data['paragraph']
        )
        
        return jsonify({"message": "Privacy entry created successfully!"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@privacy_bp.route('/show-privacies', methods=['GET'])
def show_privacies():
    try:
        privacy_model = Privacy(mongo)
        privacies = privacy_model.find_all()
        return jsonify({"message": "Privacy policies fetched successfully", "data": privacies if privacies else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@privacy_bp.route('/show-privacy/<privacy_id>', methods=['GET'])
@user_auth
@admin_auth
def show_privacy(privacy_id):
    try:
        privacy_model = Privacy(mongo)
        privacy = privacy_model.find_by_id(privacy_id)
        
        if not privacy:
            return jsonify({"message": "Privacy entry not found."}), 404
        
        return jsonify(privacy), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@privacy_bp.route('/update-privacy/<privacy_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_privacy(privacy_id):
    try:
        data = request.get_json()
        
        if not privacy_id:
            return jsonify({"message": "ID is required"}), 422
        
        privacy_model = Privacy(mongo)
        success = privacy_model.update_by_id(
            privacy_id=privacy_id,
            heading=data.get('heading'),
            paragraph=data.get('paragraph')
        )
        
        if success:
            return jsonify({"message": "Privacy entry updated successfully"}), 200
        else:
            return jsonify({"message": "Privacy entry not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@privacy_bp.route('/delete-privacy/<privacy_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_privacy(privacy_id):
    try:
        if not privacy_id:
            return jsonify({"message": "ID is required"}), 422
        
        privacy_model = Privacy(mongo)
        success = privacy_model.delete_by_id(privacy_id)
        
        if success:
            return jsonify({"message": "Privacy entry deleted successfully"}), 200
        else:
            return jsonify({"message": "Privacy entry not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500