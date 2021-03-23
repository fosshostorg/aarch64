from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


def to_object_id(obj_id: str) -> ObjectId:
    """
    Safely cast a string to BSON ObjectId, handling if the ID is invalid
    """
    try:
        return ObjectId(obj_id)
    except InvalidId:
        return ObjectId()


def get(do_async=True):
    """
    Get a database client
    :return: MongoDB client
    """

    if do_async:
        client = AsyncIOMotorClient
    else:
        client = MongoClient

    return client("mongodb://localhost:27017")["aarch64"]
