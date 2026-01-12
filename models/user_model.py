from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
import bcrypt
from bson import ObjectId
from typing import Optional, List, Dict, Any

class User:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.users  # Using 'users' as collection name

    def create_user(self, name: str, email: str, number: str, password: str, role: str = "student") -> Dict[str, Any]:
        """Create a new user"""
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_data = {
            "name": name,
            "email": email,
            "number": number,
            "password": hashed_password,
            "role": role,
            "batchNumber": 10,
            "pCertificates": [],
            "iCertificates": [],
            "cCertificates": [],
            "courses": [],
            "university": "worldsaibot",
            "resetToken": None,
            "resetTokenExpiry": None
        }
        
        result = self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        user = self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all users"""
        users = list(self.collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return users

    def update_password(self, user_id: str, new_password: str) -> bool:
        """Update user password"""
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )
        return result.modified_count > 0

    def update_field(self, user_id: str, field: str, value: Any) -> bool:
        """Update a specific field for a user"""
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {field: value}}
        )
        return result.modified_count > 0

    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update multiple fields for a user and return updated user"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                # Return the updated user
                return self.find_by_id(user_id)
            return None
        except:
            return None

    def add_course(self, user_id: str, course_data: Dict[str, Any]) -> bool:
        """Add a course to user's courses list"""
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"courses": course_data}}
        )
        return result.modified_count > 0

    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def delete_by_id(self, user_id: str) -> bool:
        """Delete user by ID"""
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0