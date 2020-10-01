# Optimizing-Public-Transportation

## Architecture 
![Architecture](https://github.com/san089/Optimizing-Public-Transportation/blob/master/docs/architecture.png)

#### Overview
In this project we construct a streaming event pipeline around Apache Kafka and its ecosystem. Using public dataset from [Chicago Transit Authority](https://www.transitchicago.com/data/) we constructed an event pipeline around Kakfa that allows to simulate and display status of train in real time.

**Arrival and Turnstiles ->** Producers that create train arrival and turnstile information into our kafka cluster. Arrivals indicate that a train has arrived at a particular station while the turnstile event indicate a passanger has entered the station. 

**Weather ->** A REST Proxy prodcer that periodically emits weather data by a REST Proxy and emits that to the kafka cluster.

**Postgres SQL and Kafka Connect ->** Extract data from stations and push it to kafka cluster. 

**Kafka status server ->** Consumes data from kafka topics and display on the UI.

![Results](https://github.com/san089/Optimizing-Public-Transportation/blob/master/docs/results.png)

#### Environment 
-   Docker (I used bitnami kafka image available [here](https://hub.docker.com/r/bitnami/kafka)
-   Python 3.7

#### Running and Testing
First make sure all the service are up and running: 
For docker use:

    docker-compose up
Docker-Compose will take 3-5 minutes to start, depending on your hardware.
Once Docker-Compose is ready, make sure the services are running by connecting to them using DOCKER URL provided below:

![](https://github.com/san089/Optimizing-Public-Transportation/blob/master/docs/services.png)

Also, you need to install requirements as well, use below command to create a virtual environment and install requirements:
1.  `cd producers`
2.  `virtualenv venv`
3.  `. venv/bin/activate`
4.  `pip install -r requirements.txt`

Same for the consumers, setup environment as below:
1.  `cd consumers`
2.  `virtualenv venv`
3.  `. venv/bin/activate`
4.  `pip install -r requirements.txt`

#### Running Simulation
Run the producers using simulation.py in producers folder:

    python simulation.py

Run the Faust Stream Processing Application:

    cd consumers
    faust -A faust_stream worker -l info

Run KSQL consumer as below:

    cd consumers
    python ksql.py

To run consumer server: 

    cd consumers
    python server.py



### Resources
[Confluent Python Client Documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/#) <br/>
[Confluent Python Client Usage and Examples](https://github.com/confluentinc/confluent-kafka-python#usage) <br/>
[REST Proxy API Reference](https://docs.confluent.io/current/kafka-rest) <br/>
[Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html) <br/>
