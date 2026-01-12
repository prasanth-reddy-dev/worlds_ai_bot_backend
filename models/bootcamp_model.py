from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Bootcamp:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.bootcamps  # Using 'bootcamps' as collection name

    def create_bootcamp(self, days: int, course_name: str, start_date: str, end_date: str, 
                       start_time: str, course_roadmap: List[List[str]], video_url: str, 
                       instructors: List[Dict[str, str]]) -> Dict[str, Any]:
        """Create a new bootcamp"""
        bootcamp_data = {
            "days": days,
            "courseName": course_name,
            "startDate": start_date,
            "endDate": end_date,
            "startTime": start_time,
            "courseRoadmap": course_roadmap,
            "videoUrl": video_url,
            "instructors": instructors
        }
        
        result = self.collection.insert_one(bootcamp_data)
        bootcamp_data["_id"] = str(result.inserted_id)
        return bootcamp_data

    def find_by_id(self, bootcamp_id: str) -> Optional[Dict[str, Any]]:
        """Find bootcamp by ID"""
        try:
            bootcamp = self.collection.find_one({"_id": ObjectId(bootcamp_id)})
            if bootcamp:
                bootcamp["_id"] = str(bootcamp["_id"])
            return bootcamp
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all bootcamps"""
        bootcamps = list(self.collection.find())
        for bootcamp in bootcamps:
            bootcamp["_id"] = str(bootcamp["_id"])
        return bootcamps

    def update_by_id(self, bootcamp_id: str, **kwargs) -> bool:
        """Update bootcamp by ID"""
        update_data = {}
        if 'days' in kwargs:
            update_data['days'] = kwargs['days']
        if 'course_name' in kwargs:
            update_data['courseName'] = kwargs['course_name']
        if 'start_date' in kwargs:
            update_data['startDate'] = kwargs['start_date']
        if 'end_date' in kwargs:
            update_data['endDate'] = kwargs['end_date']
        if 'start_time' in kwargs:
            update_data['startTime'] = kwargs['start_time']
        if 'course_roadmap' in kwargs:
            update_data['courseRoadmap'] = kwargs['course_roadmap']
        if 'video_url' in kwargs:
            update_data['videoUrl'] = kwargs['video_url']
        if 'instructors' in kwargs:
            update_data['instructors'] = kwargs['instructors']
        
        result = self.collection.update_one(
            {"_id": ObjectId(bootcamp_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, bootcamp_id: str) -> bool:
        """Delete bootcamp by ID"""
        result = self.collection.delete_one({"_id": ObjectId(bootcamp_id)})
        return result.deleted_count > 0