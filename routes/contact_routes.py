from flask import Blueprint, request, jsonify
from config.database import mongo
from models.contact_model import Contact
from middlewares.auth import user_auth, admin_auth

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/create-contact', methods=['POST'])
@user_auth
@admin_auth
def create_contact():
    try:
        data = request.get_json()
        
        required_fields = ['offer', 'heading', 'tag', 'insta', 'linkedin', 'youtube', 'channel', 'maps', 'group', 'email', 'number', 'address', 'logo']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required..."}), 422
        
        contact_model = Contact(mongo)
        new_contact = contact_model.create_contact(
            offer=data['offer'],
            heading=data['heading'],
            tag=data['tag'],
            insta=data['insta'],
            linkedin=data['linkedin'],
            youtube=data['youtube'],
            channel=data['channel'],
            maps=data['maps'],
            group=data['group'],
            email=data['email'],
            number=data['number'],
            address=data['address'],
            logo=data['logo']
        )
        
        return jsonify({"message": "Contact created successfully!", "contact": new_contact}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@contact_bp.route('/all-contacts', methods=['GET'])
def all_contacts():
    try:
        contact_model = Contact(mongo)
        contacts = contact_model.find_all()
        return jsonify({"message": "Contacts fetched successfully", "data": contacts if contacts else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@contact_bp.route('/show-contact/<contact_id>', methods=['GET'])
def show_contact(contact_id):
    try:
        contact_model = Contact(mongo)
        contact = contact_model.find_by_id(contact_id)
        
        if not contact:
            return jsonify({"message": "Contact not found"}), 404
        
        return jsonify(contact), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@contact_bp.route('/update-contact/<contact_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_contact(contact_id):
    try:
        data = request.get_json()
        
        if not contact_id:
            return jsonify({"message": "ID is required"}), 422
        
        contact_model = Contact(mongo)
        success = contact_model.update_by_id(
            contact_id=contact_id,
            offer=data.get('offer'),
            heading=data.get('heading'),
            tag=data.get('tag'),
            insta=data.get('insta'),
            linkedin=data.get('linkedin'),
            youtube=data.get('youtube'),
            channel=data.get('channel'),
            maps=data.get('maps'),
            group=data.get('group'),
            email=data.get('email'),
            number=data.get('number'),
            address=data.get('address'),
            logo=data.get('logo')
        )
        
        if success:
            return jsonify({"message": "Contact updated successfully"}), 200
        else:
            return jsonify({"message": "Contact not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@contact_bp.route('/delete-contact/<contact_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_contact(contact_id):
    try:
        if not contact_id:
            return jsonify({"message": "ID is required"}), 422
        
        contact_model = Contact(mongo)
        success = contact_model.delete_by_id(contact_id)
        
        if success:
            return jsonify({"message": "Contact deleted successfully"}), 200
        else:
            return jsonify({"message": "Contact not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500