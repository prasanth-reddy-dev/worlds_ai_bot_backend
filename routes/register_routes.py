from flask import Blueprint, request, jsonify
from config.database import mongo
from models.register_model import Register
from middlewares.auth import user_auth, admin_auth

register_bp = Blueprint('register', __name__)

@register_bp.route('/create-register', methods=['POST'])
def create_register():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'mobile', 'country', 'state', 'course']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required..."}), 422
        
        register_model = Register(mongo)
        new_register = register_model.create_register(
            name=data['name'],
            email=data['email'],
            mobile=data['mobile'],
            country=data['country'],
            state=data['state'],
            course=data['course']
        )
        
        return jsonify({"message": "User registered successfully!", "register": new_register}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@register_bp.route('/all-registers', methods=['GET'])
@user_auth
@admin_auth
def all_registers():
    try:
        register_model = Register(mongo)
        registers = register_model.find_all()
        return jsonify({"message": "Registers fetched successfully", "data": registers if registers else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@register_bp.route('/delete-register/<register_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_register(register_id):
    try:
        register_model = Register(mongo)
        success = register_model.delete_by_id(register_id)
        
        if not success:
            return jsonify({"message": "register not found"}), 404
        
        return jsonify({"message": "register deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500