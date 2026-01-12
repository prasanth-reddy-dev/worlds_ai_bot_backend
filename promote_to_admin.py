#!/usr/bin/env python3
"""
Quick script to promote a user to admin role
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/worlds_ai_bot')
client = MongoClient(MONGO_URI)
db = client.get_database()

# Get all users
users_collection = db['users']
users = list(users_collection.find({}, {'_id': 1, 'name': 1, 'email': 1, 'role': 1}))

print("\n" + "="*60)
print("EXISTING USERS:")
print("="*60)

if not users:
    print("No users found in database!")
else:
    for idx, user in enumerate(users, 1):
        print(f"\n{idx}. Name: {user.get('name', 'N/A')}")
        print(f"   Email: {user.get('email', 'N/A')}")
        print(f"   Role: {user.get('role', 'student')}")
        print(f"   ID: {user['_id']}")

    # Promote first user to admin (or you can choose)
    print("\n" + "="*60)
    print("PROMOTING FIRST USER TO ADMIN...")
    print("="*60)
    
    first_user = users[0]
    result = users_collection.update_one(
        {'_id': first_user['_id']},
        {'$set': {'role': 'admin'}}
    )
    
    if result.modified_count > 0:
        print(f"\n✅ SUCCESS! {first_user.get('email')} is now an ADMIN!")
        print(f"\nYou can now sign in with this account to access admin routes.")
    else:
        print(f"\n⚠️  User {first_user.get('email')} was already an admin or update failed.")
    
    # Show updated user
    updated_user = users_collection.find_one({'_id': first_user['_id']})
    print(f"\nUpdated role: {updated_user.get('role')}")

print("\n" + "="*60)
client.close()
