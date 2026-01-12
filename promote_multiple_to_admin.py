#!/usr/bin/env python3
"""
Promote specific user to admin by email
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/worlds_ai_bot')
client = MongoClient(MONGO_URI)
db = client.get_database()

# Promote specific users to admin
emails_to_promote = [
    'nandharapu1234@gmail.com',
    'prasanthreddy5b0@gmail.com',
    'prasanthuk123@gmail.com'
]

users_collection = db['users']

print("\n" + "="*60)
print("PROMOTING USERS TO ADMIN...")
print("="*60)

for email in emails_to_promote:
    result = users_collection.update_one(
        {'email': email},
        {'$set': {'role': 'admin'}}
    )
    
    if result.matched_count > 0:
        print(f"✅ {email} -> ADMIN")
    else:
        print(f"❌ {email} -> NOT FOUND")

print("\n" + "="*60)
print("UPDATED USER ROLES:")
print("="*60)

users = list(users_collection.find({}, {'name': 1, 'email': 1, 'role': 1}))
for user in users:
    role_icon = "👑" if user.get('role') == 'admin' else "👤"
    print(f"{role_icon} {user.get('email')} - {user.get('role', 'student')}")

print("\n" + "="*60)
client.close()
