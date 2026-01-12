from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Privacy:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.privacies  # Using 'privacies' as collection name

    def create_privacy(self, heading: str, paragraph: str) -> Dict[str, Any]:
        """Create a new privacy entry"""
        privacy_data = {
            "heading": heading,
            "paragraph": paragraph
        }
        
        result = self.collection.insert_one(privacy_data)
        privacy_data["_id"] = str(result.inserted_id)
        return privacy_data

    def find_by_id(self, privacy_id: str) -> Optional[Dict[str, Any]]:
        """Find privacy entry by ID"""
        try:
            privacy = self.collection.find_one({"_id": ObjectId(privacy_id)})
            if privacy:
                privacy["_id"] = str(privacy["_id"])
            return privacy
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all privacy entries"""
        privacies = list(self.collection.find())
        for privacy in privacies:
            privacy["_id"] = str(privacy["_id"])
        return privacies

    def update_by_id(self, privacy_id: str, heading: str = None, paragraph: str = None) -> bool:
        """Update privacy entry by ID"""
        update_data = {}
        if heading:
            update_data["heading"] = heading
        if paragraph:
            update_data["paragraph"] = paragraph
        
        result = self.collection.update_one(
            {"_id": ObjectId(privacy_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, privacy_id: str) -> bool:
        """Delete privacy entry by ID"""
        result = self.collection.delete_one({"_id": ObjectId(privacy_id)})
        return result.deleted_count > 0