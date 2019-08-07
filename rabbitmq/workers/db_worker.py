import pika
from rabbitmq import callbacks

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
    from rabbitmq import settings
    import sys
    worker = DbWorker(exchange_type=settings.DB_INSERTIONS_EXCHANGE_TYPE,
                      exchange_name=settings.DB_INSERTIONS_EXCHANGE_NAME,
                      routing_keys=sys.argv[1:],
                      callback=callbacks.db_insert_callback)
    worker.consume()