#!/usr/bin/env python3
""" This module return updated topic document base on name"""

def update_topics(mongo_collection, name, topics):
    """update topics of a school document based on the name

    Args:
        mongo_collection: The pymongo collection object
        name (str): The name of the school to update
        topics (list): The list of topics to set

    Returns:
        None
    """
    mongo_collection.update_one(
        {"name": name},
        {$set: {"topics": topics}}
    )