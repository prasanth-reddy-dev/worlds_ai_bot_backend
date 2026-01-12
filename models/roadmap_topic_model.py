from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class RoadMapTopic:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.roadmap_topics  # Using 'roadmap_topics' as collection name

    def create_roadmap_topic(self, road_map_name: str, id: str) -> Dict[str, Any]:
        """Create a new roadmap topic"""
        roadmap_topic_data = {
            "roadMapName": road_map_name,
            "id": id  # Keeping the same field name as in Node.js
        }
        
        result = self.collection.insert_one(roadmap_topic_data)
        roadmap_topic_data["_id"] = str(result.inserted_id)
        return roadmap_topic_data

    def find_by_id(self, roadmap_topic_id: str) -> Optional[Dict[str, Any]]:
        """Find roadmap topic by ID"""
        try:
            roadmap_topic = self.collection.find_one({"_id": ObjectId(roadmap_topic_id)})
            if roadmap_topic:
                roadmap_topic["_id"] = str(roadmap_topic["_id"])
            return roadmap_topic
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all roadmap topics"""
        roadmap_topics = list(self.collection.find())
        for topic in roadmap_topics:
            topic["_id"] = str(topic["_id"])
        return roadmap_topics

    def update_by_id(self, roadmap_topic_id: str, road_map_name: str = None, id: str = None) -> bool:
        """Update roadmap topic by ID"""
        update_data = {}
        if road_map_name:
            update_data["roadMapName"] = road_map_name
        if id:
            update_data["id"] = id
        
        result = self.collection.update_one(
            {"_id": ObjectId(roadmap_topic_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, roadmap_topic_id: str) -> bool:
        """Delete roadmap topic by ID"""
        result = self.collection.delete_one({"_id": ObjectId(roadmap_topic_id)})
        return result.deleted_count > 0