from bidurdb import db
import json

def db_insert_callback(ch, method, properties, body):
    print('recieved data to insert')
    data = json.loads(body)
    db.insert_scrape_results(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)
