#!/usr/bin/env python3
"""This module lists all documents in the collection"""


def list_all(mongo_collection):
    """
    This function lists all documents in a collection
    Args: 
        mongo_collection: pymongo collection object

    Return:
        empty list if no documents Or list of documents
    """

    return list(mongo_collection.find())