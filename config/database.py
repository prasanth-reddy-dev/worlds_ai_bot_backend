from flask_pymongo import PyMongo
from flask import Flask

# Initialize PyMongo
mongo = PyMongo()

def init_db(app: Flask):
    """Initialize database with the Flask app"""
    mongo.init_app(app)
    return mongo