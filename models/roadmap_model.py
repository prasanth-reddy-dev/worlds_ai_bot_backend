from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class RoadMap:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.roadmaps  # Using 'roadmaps' as collection name

    def create_roadmap(self, course_name: str, tutor_name: str, tutor_description: str, 
                      tutor_image_url: str, skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new roadmap"""
        roadmap_data = {
            "courseName": course_name,
            "tutorName": tutor_name,
            "tutorDescription": tutor_description,
            "tutorImageUrl": tutor_image_url,
            "skills": skills
        }
        
        result = self.collection.insert_one(roadmap_data)
        roadmap_data["_id"] = str(result.inserted_id)
        return roadmap_data

    def find_by_id(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Find roadmap by ID"""
        try:
            roadmap = self.collection.find_one({"_id": ObjectId(roadmap_id)})
            if roadmap:
                roadmap["_id"] = str(roadmap["_id"])
            return roadmap
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all roadmaps"""
        roadmaps = list(self.collection.find())
        for roadmap in roadmaps:
            roadmap["_id"] = str(roadmap["_id"])
        return roadmaps

    def update_by_id(self, roadmap_id: str, course_name: str = None, tutor_name: str = None, 
                    tutor_description: str = None, tutor_image_url: str = None, skills: List[Dict[str, Any]] = None) -> bool:
        """Update roadmap by ID"""
        update_data = {}
        if course_name:
            update_data["courseName"] = course_name
        if tutor_name:
            update_data["tutorName"] = tutor_name
        if tutor_description:
            update_data["tutorDescription"] = tutor_description
        if tutor_image_url:
            update_data["tutorImageUrl"] = tutor_image_url
        if skills:
            update_data["skills"] = skills
        
        result = self.collection.update_one(
            {"_id": ObjectId(roadmap_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, roadmap_id: str) -> bool:
        """Delete roadmap by ID"""
        result = self.collection.delete_one({"_id": ObjectId(roadmap_id)})
        return result.deleted_count > 0