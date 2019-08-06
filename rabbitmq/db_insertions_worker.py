import pika
from bidurdb import db
import json

def db_insert_callback(ch, method, properties, body):
    print('recieved data to insert')
    data = json.loads(body)
    db.insert_scrape_results(data)
    ch.basic_ack(delivery_tag=method.delievery_tag)

class DbWorker:
    def __init__(self, host='localhost', queue_name='', exchange_name='', exchange_type = 'direct',callback=None, routing_keys=[]):
        self.host = host
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_keys = routing_keys
        self.callback = callback
        self.__declare_connection_and_channel()
        self.__declare_exchange()
        self.__declare_and_bind_queue()

    def __declare_connection_and_channel(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def __declare_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange_name,exchange_type=self.exchange_type)

    def __declare_and_bind_queue(self):
        res = self.channel.queue_declare(queue=self.queue_name,durable=True)
        self.queue_name = res.method.queue
        if self.exchange_type == 'direct':
            for key in self.routing_keys:
                self.channel.queue_bind(exchange=self.exchange_name,queue=self.queue_name, routing_key=key)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.callback)
        self.channel.start_consuming()


if __name__ == "__main__":
    import sys, json
    proc_data = json.loads(sys.argv[1])
    exc_name = proc_data['exchange_name']
    exc_type = proc_data['exchange_type']
    routing_keys = proc_data['routing_keys']
    worker = DbWorker(exchange_name=exc_name,exchange_type=exc_type,routing_keys=routing_keys)
    worker.consume()