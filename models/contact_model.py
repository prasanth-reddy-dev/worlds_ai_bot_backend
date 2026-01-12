from flask_pymongo import PyMongo
from bson import ObjectId
from typing import Optional, List, Dict, Any

class Contact:
    def __init__(self, mongo: PyMongo):
        self.collection = mongo.db.contacts  # Using 'contacts' as collection name

    def create_contact(self, offer: str, heading: str, tag: str, insta: str, linkedin: str, 
                      youtube: str, channel: str, maps: str, group: str, email: str, 
                      number: str, address: str, logo: str) -> Dict[str, Any]:
        """Create a new contact"""
        contact_data = {
            "offer": offer,
            "heading": heading,
            "tag": tag,
            "insta": insta,
            "linkedin": linkedin,
            "youtube": youtube,
            "channel": channel,
            "maps": maps,
            "group": group,
            "email": email,
            "number": number,
            "address": address,
            "logo": logo
        }
        
        result = self.collection.insert_one(contact_data)
        contact_data["_id"] = str(result.inserted_id)
        return contact_data

    def find_by_id(self, contact_id: str) -> Optional[Dict[str, Any]]:
        """Find contact by ID"""
        try:
            contact = self.collection.find_one({"_id": ObjectId(contact_id)})
            if contact:
                contact["_id"] = str(contact["_id"])
            return contact
        except:
            return None

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all contacts"""
        contacts = list(self.collection.find())
        for contact in contacts:
            contact["_id"] = str(contact["_id"])
        return contacts

    def update_by_id(self, contact_id: str, offer: str = None, heading: str = None, tag: str = None,
                     insta: str = None, linkedin: str = None, youtube: str = None, channel: str = None,
                     maps: str = None, group: str = None, email: str = None, number: str = None,
                     address: str = None, logo: str = None) -> bool:
        """Update contact by ID"""
        update_data = {}
        if offer:
            update_data["offer"] = offer
        if heading:
            update_data["heading"] = heading
        if tag:
            update_data["tag"] = tag
        if insta:
            update_data["insta"] = insta
        if linkedin:
            update_data["linkedin"] = linkedin
        if youtube:
            update_data["youtube"] = youtube
        if channel:
            update_data["channel"] = channel
        if maps:
            update_data["maps"] = maps
        if group:
            update_data["group"] = group
        if email:
            update_data["email"] = email
        if number:
            update_data["number"] = number
        if address:
            update_data["address"] = address
        if logo:
            update_data["logo"] = logo
        
        result = self.collection.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_by_id(self, contact_id: str) -> bool:
        """Delete contact by ID"""
        result = self.collection.delete_one({"_id": ObjectId(contact_id)})
        return result.deleted_count > 0