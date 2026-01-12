from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Test:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.tests  # Using 'tests' as collection name

    def create_test(self, question: str, test_cases: List[Dict[str, str]], youtube_url: str = None) -> Dict[str, Any]:
        """Create a new test entry"""
        test_data = {
            "question": question,
            "test": test_cases,  # Keeping the same field name as in Node.js
            "youtube_url": youtube_url or ""
        }
        
        result = self.collection.insert_one(test_data)
        test_data["_id"] = str(result.inserted_id)
        return test_data

    def find_by_id(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Find test entry by ID"""
        try:
            test = self.collection.find_one({"_id": ObjectId(test_id)})
            if test:
                test["_id"] = str(test["_id"])
            return test
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all test entries"""
        tests = list(self.collection.find())
        for test in tests:
            test["_id"] = str(test["_id"])
        return tests

    def update_by_id(self, test_id: str, question: str = None, test_cases: List[Dict[str, str]] = None, youtube_url: str = None) -> bool:
        """Update test entry by ID"""
        update_data = {}
        if question:
            update_data["question"] = question
        if test_cases:
            update_data["test"] = test_cases
        if youtube_url is not None:
            update_data["youtube_url"] = youtube_url
        
        result = self.collection.update_one(
            {"_id": ObjectId(test_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, test_id: str) -> bool:
        """Delete test entry by ID"""
        result = self.collection.delete_one({"_id": ObjectId(test_id)})
        return result.deleted_count > 0