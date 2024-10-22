#!/usr/bin/env python3
"""This module return a updated collection"""

def insert_school(mongo_collection, **kwargs):
    """
    This function inserts a new document in a collection

    Args:
        mongo_collection: pymongo collection object
        kwargs: keyword representing the document object

    Return: a document's new _id
    """
    new_document = mongo_collection.insertOne(kwargs)
    return new_document.inserted_id