from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Course:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.courses  # Using 'courses' as collection name

    def create_course(self, course_name: str, image_url: str, price: int, duration: int, 
                     enrolled: int, status: str, badge: str, hours: int, next_id: str, 
                     recording_id: str, coupon: str = None) -> Dict[str, Any]:
        """Create a new course"""
        course_data = {
            "courseName": course_name,
            "imageUrl": image_url,
            "price": price,
            "duration": duration,
            "enrolled": enrolled,
            "status": status,
            "badge": badge,
            "hours": hours,
            "nextId": next_id,
            "recordingId": recording_id,
            "coupon": coupon.upper() if coupon else None  # Store in uppercase for case-insensitive matching
        }
        
        result = self.collection.insert_one(course_data)
        course_data["_id"] = str(result.inserted_id)
        return course_data

    def find_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Find course by ID"""
        try:
            course = self.collection.find_one({"_id": ObjectId(course_id)})
            if course:
                course["_id"] = str(course["_id"])
            return course
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all courses"""
        courses = list(self.collection.find())
        for course in courses:
            course["_id"] = str(course["_id"])
        return courses

    def update_by_id(self, course_id: str, **kwargs) -> bool:
        """Update course by ID"""
        update_data = {key: value for key, value in kwargs.items() if value is not None}
        result = self.collection.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, course_id: str) -> bool:
        """Delete course by ID"""
        result = self.collection.delete_one({"_id": ObjectId(course_id)})
        return result.deleted_count > 0