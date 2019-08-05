import pymongo
import bidurdb.settings as bidurdb_settings
from collections import defaultdict
import time

def __get_db_instance():
    return pymongo.MongoClient(bidurdb_settings.DB_URL)[bidurdb_settings.DB_NAME]


def is_collection_exists(collection_name):
    db = __get_db_instance()
    return collection_name in db.list_collection_names()

def __insert_results_to_collection(results_by_keywords):
    db = __get_db_instance()
    for keyword,results in results_by_keywords.items():
        collection_name = keyword if keyword.strip() != '' else bidurdb_settings.NO_KEYWORDS_COLLECTION_NAME
        if not is_collection_exists(collection_name):
            collection = db.create_collection(collection_name)
        else: collection = db.get_collection(collection_name)
        for doc in results:
            try:
                doc['timestamp'] = time.time() #add timestamp for each document added
                collection.insert_one(document=doc)
            except pymongo.errors.DuplicateKeyError:
                continue


def find_results_by_keyword(keyword):
    db = __get_db_instance()
    results_list = []
    collections_names_containing_keyword = [name for name in db.list_collection_names() if keyword in name]
    relevant_collections_list = [db.get_collection(name) for name in collections_names_containing_keyword]
    for relevant_collection in relevant_collections_list:
        results_list.extend([doc for doc in relevant_collection.find()])
    collection = db.get_collection(bidurdb_settings.NO_KEYWORDS_COLLECTION_NAME)
    query = {'title': {'$regex':'*{}*'.format(keyword) }} #TODO: Fix query so it works! returns none for now
    for doc in collection.find(query): results_list.append(doc)
    return results_list

def insert_scrape_results(results_list):
    results_by_keywords = defaultdict(list)
    for a_results_list in results_list:
        for result in a_results_list:
            results_by_keywords[result['keyword']].append(result)
            __insert_results_to_collection(results_by_keywords)


