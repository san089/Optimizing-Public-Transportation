"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            "ZOOKEEPER_URL" : "localhost:2181",
            "BROKER_URL" : "localhost:9092",
            "SCHEMA_REGISTRY_URL" : "localhost:8081"
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        # TODO: Configure the AvroProducer
        self.producer = AvroProducer({
            'bootstrap.servers': self.broker_properties.get("BROKER_URL"),
            'schema.registry.url' : self.broker_properties.get("SCHEMA_REGISTRY_URL")
            },
            default_key_schema=self.key_schema, 
            default_value_schema=self.value_schema
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        # TODO: Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        #
        #
        print("Inside Topic Creation.....")
        adminclient = AdminClient({'bootstrap.servers': self.broker_properties.get("BROKER_URL")})
        
        topics = adminclient.list_topics(timeout=10).topics
        print(f"Already existing topics : {[keys for keys in topics.keys()]}")
        
        if self.topic_name in topics.keys():
            print(f"Topic {self.topic_name} already exists!!")
            return
        
        newtopic = NewTopic(
            self.topic_name, 
            num_partitions = self.num_partitions,
            replication_factor = self.num_replicas 
        )
        futures = adminclient.create_topics([newtopic])
        
        
        for topic,future in futures.items():
            try:
                future.result()
                print("topics created")
            except:
                print(f"failed to create topic {topic_name}: {e}")
        
        return
        
        logger.info("topic creation kafka integration incomplete - skipping")

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #
        
        
        logger.info("producer close incomplete - skipping")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))

    
p = Producer("test", None)