from confluent_kafka.admin import AdminClient

client = AdminClient({"bootstrap.servers": "PLAINTEXT://localhost:9092"})

def topic_exists(topic):
    """Checks if the given topic exists in Kafka"""
    topic_metadata = client.list_topics(timeout=5)
    return topic in topic_metadata.topics

def contains_substring(to_test, substr):
    _before, match, _after = to_test.partition(substr)
    return len(match) > 0

def topic_pattern_match(pattern):
    """
        Takes a string `pattern`
        Returns `True` if one or more topic names contains substring `pattern`.
        Returns `False` if not.
    """
    topic_metadata = client.list_topics()
    topics = topic_metadata.topics
    filtered_topics = {key: value for key, value in topics.items() if contains_substring(key, pattern)}
    return len(filtered_topics) > 0
