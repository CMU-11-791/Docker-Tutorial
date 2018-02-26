# Docker Tutorial

This is an example project that implements a number of services running in Docker containers that communicate via RabbitMQ message queues.  The goal of this tutorial is to demonstrate implementing a service and deploying it via Docker with

## Prerequisites

It is recommended that you create a *VirtualEnv* for this project.

```
$> virtualenv .venv
$> source .venv/bin/activate
```

Then we need to install the *deiis* package which contains classes for managing RabbitMQ message queues.

```
$> cd deiis
$> python setup.py install
```

## Start RabbitMQ

The RabbitMQ server is available as a Docker image so no installation or setup is required.  We can simply launch the container and start using the server.

```
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management
```

Once the RabbitMQ server has started you can login to its management console at http://localhost:15672 (username: *guest*, password: *guest*). We won't be using the RabbitMQ management console, but it is useful to check if your services are connected to the server and watch how many messages are flowing through the server.

### Get The IP Address of RabbitMQ

Services running on the same machine as the RabbitMQ server can access the server via *localhost*.  However, services running inside Docker containers are **not** on the *same machine* as the RabbitMQ server.  That is, for services running in a Docker container *localhost* is the Docker container, not the machine running the Docker container.  Therefore we need to know what IP address has assigned to the RabbitMQ server.  Services running in Docker will be able to access RabbitMQ via this IP address.

To view information on the network that Docker has created.

```
docker network inspect bridge
```

In the JSON that is displayed will be a *Containers* section with information about each running container.  In particular we need to make a note of the *IPv4Address* assigned to our *rabbit* container.

```json
"Containers": {
    "61b390c1f1643c0ed5aeb3791b3ef00d70f8cf0d63c09d3f8c1feb2dbf176172": {
        "Name": "rabbit",
        "EndpointID": "4f056e9f757f3b940039c9988c731581a0e6ceec09dcb16d63db18b5c300c09f",
        "MacAddress": "02:42:ac:11:00:02",
        "IPv4Address": "172.17.0.2/16",
        "IPv6Address": ""
    }
}
```

Here we can see that Docker has assigned the IP address 172.17.0.2 to my RabbitMQ server.  This is the IP address that services running in a Docker container will use to access the RabbitMQ server.

## Project Layout

TDB

## Building The Project

Each module (service) contains a *Makefile* that is used to build the Docker image for the service:

```
$> cd Service1
$> make
```

The top level of the project also contains a Makefile will simply calls *make* for each of the services.

## Running The Services

```
$> docker run -d -e HOST=$RABBIT_HOST --name one tutorial/one
$> docker run -d -e HOST=$RABBIT_HOST --name two tutorial/two
$> docker run -d -e HOST=$RABBIT_HOST --name three tutorial/three
$> docker run -d -e HOST=$RABBIT_HOST --name printer -v /tmp:/var/log tutorial/printer
```

A Bash script is also provided that starts all of the containers.

```
$> ./start.sh
```

### Running A Pipeline

```
python pipeline.py one two three two one one three print
```

### Stopping The Services


Send the poison pill (shutdown message) to all services:

```
$> ./stop.py
```

Stop individual services by specifying just the message queues that the poison pill should be sent toL

```
$> ./stop.py one printer
```
