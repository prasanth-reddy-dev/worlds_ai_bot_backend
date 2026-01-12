from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Job:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.jobs  # Using 'jobs' as collection name

    def create_job(self, experience: str, job_role: str, work_type: str) -> Dict[str, Any]:
        """Create a new job"""
        job_data = {
            "experience": experience,
            "jobRole": job_role,  # Keeping the same field name as in Node.js
            "workType": work_type
        }
        
        result = self.collection.insert_one(job_data)
        job_data["_id"] = str(result.inserted_id)
        return job_data

    def find_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Find job by ID"""
        try:
            job = self.collection.find_one({"_id": ObjectId(job_id)})
            if job:
                job["_id"] = str(job["_id"])
            return job
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all jobs"""
        jobs = list(self.collection.find())
        for job in jobs:
            job["_id"] = str(job["_id"])
        return jobs

    def update_by_id(self, job_id: str, experience: str = None, job_role: str = None, work_type: str = None) -> bool:
        """Update job by ID"""
        update_data = {}
        if experience:
            update_data["experience"] = experience
        if job_role:
            update_data["jobRole"] = job_role
        if work_type:
            update_data["workType"] = work_type
        
        result = self.collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, job_id: str) -> bool:
        """Delete job by ID"""
        result = self.collection.delete_one({"_id": ObjectId(job_id)})
        return result.deleted_count > 0