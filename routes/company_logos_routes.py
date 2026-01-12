from flask import Blueprint, request, jsonify
from config.database import mongo
from models.company_logos_model import CompanyLogos
from middlewares.auth import user_auth, admin_auth

company_logos_bp = Blueprint('company_logos', __name__)

@company_logos_bp.route('/create-logo', methods=['POST'])
@user_auth
@admin_auth
def create_logo():
    try:
        data = request.get_json()
        
        required_fields = ['companyName', 'logoUrl']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "Company name and logo URL are required"}), 422
        
        logo_model = CompanyLogos(mongo)
        new_logo = logo_model.create_logo(
            company_name=data['companyName'],
            logo_url=data['logoUrl']
        )
        
        return jsonify({"message": "Logo created successfully!", "logo": new_logo}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@company_logos_bp.route('/all-logos', methods=['GET'])
def all_logos():
    try:
        logo_model = CompanyLogos(mongo)
        logos = logo_model.find_all()
        return jsonify({"message": "Logos fetched successfully", "data": logos if logos else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@company_logos_bp.route('/show-companies', methods=['GET'])
def show_companies():
    """Endpoint to match frontend call"""
    try:
        logo_model = CompanyLogos(mongo)
        logos = logo_model.find_all()
        return jsonify({"message": "Companies fetched successfully", "data": logos if logos else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@company_logos_bp.route('/show-logo/<logo_id>', methods=['GET'])
def show_logo(logo_id):
    try:
        logo_model = CompanyLogos(mongo)
        logo = logo_model.find_by_id(logo_id)
        
        if not logo:
            return jsonify({"message": "Logo not found"}), 404
        
        return jsonify(logo), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@company_logos_bp.route('/show-company/<logo_id>', methods=['GET'])
def show_company(logo_id):
    """Endpoint to match frontend call"""
    try:
        logo_model = CompanyLogos(mongo)
        logo = logo_model.find_by_id(logo_id)
        
        if not logo:
            return jsonify({"message": "Company not found"}), 404
        
        return jsonify(logo), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@company_logos_bp.route('/update-logo/<logo_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_logo(logo_id):
    try:
        data = request.get_json()
        
        if not logo_id:
            return jsonify({"message": "ID is required"}), 422
        
        logo_model = CompanyLogos(mongo)
        success = logo_model.update_by_id(
            logo_id=logo_id,
            company_name=data.get('companyName'),
            logo_url=data.get('logoUrl')
        )
        
        if success:
            return jsonify({"message": "Logo updated successfully"}), 200
        else:
            return jsonify({"message": "Logo not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@company_logos_bp.route('/update-company/<logo_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_company(logo_id):
    """Endpoint to match frontend call"""
    try:
        data = request.get_json()
        
        if not logo_id:
            return jsonify({"message": "ID is required"}), 422
        
        logo_model = CompanyLogos(mongo)
        success = logo_model.update_by_id(
            logo_id=logo_id,
            company_name=data.get('companyName'),
            logo_url=data.get('logo')
        )
        
        if success:
            return jsonify({"message": "Company updated successfully"}), 200
        else:
            return jsonify({"message": "Company not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@company_logos_bp.route('/delete-logo/<logo_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_logo(logo_id):
    try:
        if not logo_id:
            return jsonify({"message": "ID is required"}), 422
        
        logo_model = CompanyLogos(mongo)
        success = logo_model.delete_by_id(logo_id)
        
        if success:
            return jsonify({"message": "Logo deleted successfully"}), 200
        else:
            return jsonify({"message": "Logo not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@company_logos_bp.route('/delete-company/<logo_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_company(logo_id):
    """Endpoint to match frontend call"""
    try:
        if not logo_id:
            return jsonify({"message": "ID is required"}), 422
        
        logo_model = CompanyLogos(mongo)
        success = logo_model.delete_by_id(logo_id)
        
        if success:
            return jsonify({"message": "Company deleted successfully"}), 200
        else:
            return jsonify({"message": "Company not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
