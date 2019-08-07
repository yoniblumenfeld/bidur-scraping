"""
RabbitMQ
settings
"""
import os

DB_INSERTIONS_EXCHANGE_NAME = 'db_insertion'
DB_INSERTIONS_EXCHANGE_TYPE = 'direct'
DB_INSERTIONS_WORKER_PATH = os.path.join(os.getcwd(),'rabbitmq','db_worker.py')
ROUTING_KEYS = ['tzavta','zappa','cameri','barby'] #according to scrapers names