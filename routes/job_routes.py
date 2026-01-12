from flask import Blueprint, request, jsonify
from config.database import mongo
from models.job_model import Job
from middlewares.auth import user_auth, admin_auth

job_bp = Blueprint('job', __name__)

@job_bp.route('/create-job', methods=['POST'])
@user_auth
@admin_auth
def create_job():
    try:
        data = request.get_json()
        
        required_fields = ['experience', 'jobRole', 'workType']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"message": "All fields are required..."}), 422
        
        job_model = Job(mongo)
        new_job = job_model.create_job(
            experience=data['experience'],
            job_role=data['jobRole'],
            work_type=data['workType']
        )
        
        return jsonify({"message": "Job created successfully!!"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@job_bp.route('/show-jobs', methods=['GET'])
def show_jobs():
    try:
        job_model = Job(mongo)
        jobs = job_model.find_all()
        return jsonify({"message": "Jobs fetched successfully", "data": jobs if jobs else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Alias endpoint to match frontend call
@job_bp.route('/all-jobs', methods=['GET'])
def all_jobs():
    """Endpoint to match frontend call"""
    try:
        job_model = Job(mongo)
        jobs = job_model.find_all()
        return jsonify({"message": "Jobs fetched successfully", "data": jobs if jobs else []}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@job_bp.route('/show-job/<job_id>', methods=['GET'])
@user_auth
@admin_auth
def show_job(job_id):
    try:
        job_model = Job(mongo)
        job = job_model.find_by_id(job_id)
        
        if not job:
            return jsonify({"message": "Job not found"}), 404
        
        return jsonify(job), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@job_bp.route('/update-job/<job_id>', methods=['PUT'])
@user_auth
@admin_auth
def update_job(job_id):
    try:
        data = request.get_json()
        
        if not job_id:
            return jsonify({"message": "ID is required"}), 422
        
        job_model = Job(mongo)
        success = job_model.update_by_id(
            job_id=job_id,
            experience=data.get('experience'),
            job_role=data.get('jobRole'),
            work_type=data.get('workType')
        )
        
        if success:
            return jsonify({"message": "Job updated successfully"}), 200
        else:
            return jsonify({"message": "Job not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@job_bp.route('/delete-job/<job_id>', methods=['DELETE'])
@user_auth
@admin_auth
def delete_job(job_id):
    try:
        if not job_id:
            return jsonify({"message": "ID is required"}), 422
        
        job_model = Job(mongo)
        success = job_model.delete_by_id(job_id)
        
        if success:
            return jsonify({"message": "Job deleted successfully"}), 200
        else:
            return jsonify({"message": "Job not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500