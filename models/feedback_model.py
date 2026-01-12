from config.database import mongo
from bson import ObjectId
from datetime import datetime

class Feedback:
    def __init__(self, mongo):
        self.db = mongo.db
        self.collection = self.db.feedbacks

    def create_feedback(self, name, email, mobile, message):
        feedback = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "message": message,
            "status": "pending",  # pending, reviewed, resolved
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = self.collection.insert_one(feedback)
        feedback["_id"] = str(result.inserted_id)
        return feedback

    def find_all(self):
        feedbacks = list(self.collection.find().sort("createdAt", -1))
        for feedback in feedbacks:
            feedback["_id"] = str(feedback["_id"])
        return feedbacks

    def find_by_id(self, feedback_id):
        feedback = self.collection.find_one({"_id": ObjectId(feedback_id)})
        if feedback:
            feedback["_id"] = str(feedback["_id"])
        return feedback

    def update_status(self, feedback_id, status):
        result = self.collection.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": {"status": status, "updatedAt": datetime.utcnow()}}
        )
        return result.modified_count > 0

    def delete_by_id(self, feedback_id):
        result = self.collection.delete_one({"_id": ObjectId(feedback_id)})
        return result.deleted_count > 0
