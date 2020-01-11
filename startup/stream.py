from dataclasses import asdict, dataclass, field
import json
import time
import random

import requests
from confluent_kafka import avro, Consumer, Producer
from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient
from faker import Faker


faker = Faker()
REST_PROXY_URL = "http://localhost:8082"


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))


@dataclass
class User:
    username: str = field(default_factory=faker.user_name)
    email: str = field(default_factory=faker.email)
    phone_number: str = field(default_factory=faker.phone_number)
    address: str = field(default_factory=faker.address)


def produce():
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": "PLAINTEXT://localhost:9092"})

    # Create an assortment of users by currency and produce them into Kafka
    currency_freq = {
        "USD": 100,
        "GBP": 25,
        "RMB": 90,
        "INR": 80,
        "EUR": 100,
        "CAD": 45,
        "AUD": 45,
        "NZD": 20,
        "ISK": 5,
        "RUB": 70,
        "NOK": 15,
    }
    currency_users = []
    for currency_code, frq in currency_freq.items():
        for _ in range(frq):
            user = User()
            currency_users.append((currency_code, user))
            user_data = json.dumps(asdict(user))
            p.produce("com.udacity.streams.users", value=user_data, key=user.username)

    # Now start simulating purchase events for the users
    while True:
        currency_type, user = random.choice(currency_users)
        purchase = Purchase(username=user.username, currency=currency_type)
        p.produce(
            "com.udacity.streams.purchases",
            value=json.dumps(asdict(purchase)),
            key=user.username,
        )
        time.sleep(0.1)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        produce()
    except KeyboardInterrupt as e:
        print("shutting down")


if __name__ == "__main__":
    main()