from flask import Blueprint, request, jsonify
from config.database import mongo
from models.test_model import Test
from middlewares.auth import user_auth, admin_auth

test_bp = Blueprint('test', __name__)

@test_bp.route('/create-test', methods=['POST'])
@user_auth
@admin_auth
def create_test():
    try:
        data = request.get_json()
        
        required_fields = ['question', 'test']
        if not data or not all(field in data for field in required_fields) or not isinstance(data['test'], list) or len(data['test']) == 0:
            return jsonify({"message": "Question and at least one test case (input/output) are required..."}), 422
        
        # Validate each test case
        for item in data['test']:
            if not all(field in item for field in ['input', 'output']):
                return jsonify({"message": "Each test case must have input and output..."}), 422
        
        test_model = Test(mongo)
        new_test = test_model.create_test(
            question=data['question'],
            test_cases=data['test'],
            youtube_url=data.get('youtube_url', '')
        )
        
        return jsonify({"message": "Test created successfully!", "test": new_test}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@test_bp.route('/all-tests', methods=['GET'])
@user_auth
def all_tests():
    try:
        test_model = Test(mongo)
        tests = test_model.find_all()
        return jsonify({"message": "Tests fetched successfully", "data": tests if tests else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@test_bp.route('/show-test/<test_id>', methods=['GET'])
@user_auth
def show_test(test_id):
    try:
        test_model = Test(mongo)
        test = test_model.find_by_id(test_id)
        
        if not test:
            return jsonify({"message": "Test not found"}), 404
        
        return jsonify(test), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@test_bp.route('/update-test/<test_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_test(test_id):
    try:
        data = request.get_json()
        
        if not test_id:
            return jsonify({"message": "ID is required"}), 422
        
        test_model = Test(mongo)
        success = test_model.update_by_id(
            test_id=test_id,
            question=data.get('question'),
            test_cases=data.get('test'),
            youtube_url=data.get('youtube_url')
        )
        
        if success:
            return jsonify({"message": "Test updated successfully"}), 200
        else:
            return jsonify({"message": "Test not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@test_bp.route('/delete-test/<test_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_test(test_id):
    try:
        if not test_id:
            return jsonify({"message": "ID is required"}), 422
        
        test_model = Test(mongo)
        success = test_model.delete_by_id(test_id)
        
        if success:
            return jsonify({"message": "Test deleted successfully"}), 200
        else:
            return jsonify({"message": "Test not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500