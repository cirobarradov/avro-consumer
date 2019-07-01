import os
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

class StringKeyAvroConsumer(AvroConsumer):

    def __init__(self, config):
        super(StringKeyAvroConsumer, self).__init__(config)

    def poll(self, timeout=None):
        """
        This is an overriden method from AvroConsumer class. This handles message
        deserialization using avro schema for the value only.

        @:param timeout
        @:return message object with deserialized key and value as dict objects
        """
        if timeout is None:
            timeout = -1
        message = super(AvroConsumer, self).poll(timeout)
        if message is None:
            return None
        if not message.value() and not message.key():
            return message
        if not message.error():
            if message.value() is not None:
                decoded_value = self._serializer.decode_message(message.value())
                message.set_value(decoded_value)
            # Don't try to decode the key
        return message


c = StringKeyAvroConsumer({
    'bootstrap.servers': os.environ['BROKER_LIST'],
    'group.id': 'topics2stdout',
    'schema.registry.url': 'http://{}:{}'.format(os.environ['SCHEMA_HOST'],os.environ['SCHEMA_PORT'])})
c.subscribe(os.environ['TOPIC_LIST'].split(","))

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue
    res = dict()
    res['payload']=msg.value()
    res['topic']=msg.topic()
    print(res)

c.close()
