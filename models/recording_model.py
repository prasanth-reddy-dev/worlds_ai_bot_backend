from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Recording:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.recordings  # Using 'recordings' as collection name

    def create_recording(self, batch_number: int, recordings: List[Dict[str, str]], status: bool = True) -> Dict[str, Any]:
        """Create a new recording"""
        recording_data = {
            "batchNumber": batch_number,
            "recordings": recordings,
            "status": status  # Active by default
        }
        
        result = self.collection.insert_one(recording_data)
        recording_data["_id"] = str(result.inserted_id)
        return recording_data

    def find_by_id(self, recording_id: str) -> Optional[Dict[str, Any]]:
        """Find recording by ID"""
        try:
            recording = self.collection.find_one({"_id": ObjectId(recording_id)})
            if recording:
                recording["_id"] = str(recording["_id"])
            return recording
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all recordings"""
        recordings = list(self.collection.find())
        for recording in recordings:
            recording["_id"] = str(recording["_id"])
        return recordings

    def update_by_id(self, recording_id: str, batch_number: int = None, recordings: List[Dict[str, str]] = None, status: bool = None) -> bool:
        """Update recording by ID"""
        update_data = {}
        if batch_number is not None:
            update_data["batchNumber"] = batch_number
        if recordings is not None:
            update_data["recordings"] = recordings
        if status is not None:
            update_data["status"] = status
        
        result = self.collection.update_one(
            {"_id": ObjectId(recording_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, recording_id: str) -> bool:
        """Delete recording by ID"""
        result = self.collection.delete_one({"_id": ObjectId(recording_id)})
        return result.deleted_count > 0