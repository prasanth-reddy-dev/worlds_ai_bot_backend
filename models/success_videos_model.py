from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class SuccessVideos:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.success_videos

    def create_success_video(self, video_url: str, job_role: str, name: str, package: str, company_name: str) -> Dict[str, Any]:
        """Create a new success video"""
        video_data = {
            "videoUrl": video_url,
            "jobRole": job_role,
            "name": name,
            "package": package,
            "companyName": company_name
        }
        
        result = self.collection.insert_one(video_data)
        video_data["_id"] = str(result.inserted_id)
        return video_data

    def find_by_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Find success video by ID"""
        try:
            video = self.collection.find_one({"_id": ObjectId(video_id)})
            if video:
                video["_id"] = str(video["_id"])
            return video
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all success videos"""
        videos = list(self.collection.find())
        for video in videos:
            video["_id"] = str(video["_id"])
        return videos

    def update_by_id(self, video_id: str, video_url: str = None, job_role: str = None, name: str = None, package: str = None, company_name: str = None) -> bool:
        """Update success video by ID"""
        update_data = {}
        if video_url:
            update_data["videoUrl"] = video_url
        if job_role:
            update_data["jobRole"] = job_role
        if name:
            update_data["name"] = name
        if package:
            update_data["package"] = package
        if company_name:
            update_data["companyName"] = company_name
        
        result = self.collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, video_id: str) -> bool:
        """Delete success video by ID"""
        result = self.collection.delete_one({"_id": ObjectId(video_id)})
        return result.deleted_count > 0
