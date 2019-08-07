import pika,json

class DbProducer:
    def __init__(self, host='localhost', exchange_name='', exchange_type = 'direct',callback=None,routing_key=None):
        self.host = host
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        if self.exchange_type == 'direct' and routing_key is None:
            raise ValueError('Routing key parameter cant be none if using direct exchange type')
        self.callback = callback
        self.__declare_connection_and_channel()
        self.__declare_exchange()

    def __declare_connection_and_channel(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def __declare_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange_name,exchange_type=self.exchange_type)

    def publish(self,data):
        json_data = json.dumps(data)
        self.channel.basic_publish(exchange=self.exchange_name,routing_key=self.routing_key,body=json_data)
    def close(self):
        self.connection.close()

