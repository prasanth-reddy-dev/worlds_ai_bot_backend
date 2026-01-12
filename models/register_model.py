from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Register:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.registers  # Using 'registers' as collection name

    def create_register(self, name: str, email: str, mobile: str, country: str, state: str, course: str) -> Dict[str, Any]:
        """Create a new register entry"""
        register_data = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "country": country,
            "state": state,
            "course": course
        }
        
        result = self.collection.insert_one(register_data)
        register_data["_id"] = str(result.inserted_id)
        return register_data

    def find_by_id(self, register_id: str) -> Optional[Dict[str, Any]]:
        """Find register by ID"""
        try:
            register = self.collection.find_one({"_id": ObjectId(register_id)})
            if register:
                register["_id"] = str(register["_id"])
            return register
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all registers"""
        registers = list(self.collection.find())
        for register in registers:
            register["_id"] = str(register["_id"])
        return registers

    def delete_by_id(self, register_id: str) -> bool:
        """Delete register by ID"""
        result = self.collection.delete_one({"_id": ObjectId(register_id)})
        return result.deleted_count > 0