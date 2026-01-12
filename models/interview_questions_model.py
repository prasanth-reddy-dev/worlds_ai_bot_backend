from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class InterviewQuestions:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.interview_questions

    def create_interview_question(self, topic: str, questions: list) -> Dict[str, Any]:
        """Create a new interview question set with topic and questions array"""
        interview_data = {
            "topic": topic,
            "questions": questions
        }
        
        result = self.collection.insert_one(interview_data)
        interview_data["_id"] = str(result.inserted_id)
        return interview_data

    def find_by_id(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """Find interview question by ID"""
        try:
            interview = self.collection.find_one({"_id": ObjectId(interview_id)})
            if interview:
                interview["_id"] = str(interview["_id"])
            return interview
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all interview questions"""
        interviews = list(self.collection.find())
        for interview in interviews:
            interview["_id"] = str(interview["_id"])
        return interviews

    def update_by_id(self, interview_id: str, topic: str = None, questions: list = None) -> bool:
        """Update interview question set by ID"""
        update_data = {}
        if topic:
            update_data["topic"] = topic
        if questions:
            update_data["questions"] = questions
        
        result = self.collection.update_one(
            {"_id": ObjectId(interview_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, interview_id: str) -> bool:
        """Delete interview question by ID"""
        result = self.collection.delete_one({"_id": ObjectId(interview_id)})
        return result.deleted_count > 0
