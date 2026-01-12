from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class CompanyLogos:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.company_logos

    def create_logo(self, company_name: str, logo_url: str) -> Dict[str, Any]:
        """Create a new company logo"""
        logo_data = {
            "companyName": company_name,
            "logoUrl": logo_url
        }
        
        result = self.collection.insert_one(logo_data)
        logo_data["_id"] = str(result.inserted_id)
        return logo_data

    def find_by_id(self, logo_id: str) -> Optional[Dict[str, Any]]:
        """Find company logo by ID"""
        try:
            logo = self.collection.find_one({"_id": ObjectId(logo_id)})
            if logo:
                logo["_id"] = str(logo["_id"])
            return logo
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all company logos"""
        logos = list(self.collection.find())
        for logo in logos:
            logo["_id"] = str(logo["_id"])
        return logos

    def update_by_id(self, logo_id: str, company_name: str = None, logo_url: str = None) -> bool:
        """Update company logo by ID"""
        update_data = {}
        if company_name:
            update_data["companyName"] = company_name
        if logo_url:
            update_data["logoUrl"] = logo_url
        
        result = self.collection.update_one(
            {"_id": ObjectId(logo_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, logo_id: str) -> bool:
        """Delete company logo by ID"""
        result = self.collection.delete_one({"_id": ObjectId(logo_id)})
        return result.deleted_count > 0
