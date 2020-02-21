"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)


KSQL_URL = "http://localhost:8088"

KSQL_STATEMENT = """CREATE TABLE turnstile (STATION_ID INTEGER, STATION_NAME VARCHAR, LINE VARCHAR) WITH ( KAFKA_TOPIC='turnstile', VALUE_FORMAT='avro', key='STATION_ID');
CREATE TABLE turnstile_summary WITH (KAFKA_TOPIC='TURNSTILE_SUMMARY',VALUE_FORMAT='json') AS SELECT STATION_ID, STATION_NAME, COUNT(STATION_ID) as COUNT FROM turnstile GROUP BY STATION_ID, STATION_NAME;
"""

def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")
    data = json.dumps(
            {
                "ksql": json.dumps(KSQL_STATEMENT),
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        )
    
    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json.dumps(
            {
                "ksql": KSQL_STATEMENT,
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        ),
    )

    # Ensure that a 2XX status code was returned
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print(e)
        logger.info("Error with KSQL POST request.")


if __name__ == "__main__":
    execute_statement()
