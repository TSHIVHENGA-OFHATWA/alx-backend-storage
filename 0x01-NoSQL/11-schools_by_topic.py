#!/usr/bin/env python3
"""This module return lists of school by topic"""


def schools_by_topic(mongo_collection, topic):
    """ Return a list of schools having a specific topic

    Args:
        mongo_collection: The pymongo collection object
        topic (str): The topic to search for

    Returns:
        A list of schools that have the specified topic
    """
    results = mongo_collection.find({"topics": topic})
    return list(results)
