# Docker Tutorial

This is an example project that implements a number of services running in Docker containers that communicate via RabbitMQ message queues.  The goal of this tutorial is to demonstrate implementing a service and deploying it via Docker using the same classes and framework used for the BioASQ Summarization challenge.

## Prerequisites

This tutorial assumes that you have [Docker installed](https://store.docker.com/search?type=edition&offering=community) on your machine.

## TL;DR  (Too Long ; Didn't Read)

```
#!/usr/bin/env bash

git clone https://github.com/cmu-11-791/Docker-Tutorial.git [1]
cd Docker-Tutorial
virtualenv .venv                                            [2]
source .venv/bin/activate
cd deiis                                                    [3]
python setup.py install
cd ../
make                                                        [4]
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management [5]
./start.sh                                                  [6]
python pipeline.py one two three two one print              [7]
./stop.sh                                                   [8]
cat /tmp/deiis-tutorial.log                                 [9]
```

1. Clone the repository<br/>
   `git clone https://github.com/cmu-11-791/Docker-Tutorial.git`<br/>
   `cd Docker-Tutorial`
1. Create a virtual environment and activate it.<br/>
  `virtualenv .venv`<br/>
  `source .venv/bin/activate`
1. Install the *deiis* module<br/>
  `cd deiis`<br/>
  `python setup.py install`<br/>
  `cd ../`
1. Build the Docker images<br/>
  `make`
1. Start the RabbitMQ server<br/>
  `docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management`
1. Start the containers<br/>
  `./start.sh`
1. Run a pipeline<br/>
  `python pipeline.py one two three two one print`
1. Stop all the containers<br/>
  `./stop.sh`
1. View the output<br/>
  `cat /tmp/deiis-tutorial.log`

**Troubleshooting**

The above should work in the majority of instances.  However, the `start.sh` script expects that Docker will assign the IP address 172.17.0.2 to the RabbitMQ server, which it usually does. If the containers are not starting [check the IP address assigned to the RabbitMQ server](#rabbit-ip).

If Docker reports an error about a container name already in use you will need to delete (rm) that container before running it again.

```
docker: Error response from daemon: Conflict. The container name "XYZ" is already in use by container
$> docker rm XYZ
```

You can use the `./cleanup.sh` script to delete all stopped containers.

# The Long Version

## Setup

It is recommendeded that you create a *virtual environment* for this project and then install the *deiis* package.

```
$> virtualenv .venv
$> source .venv/bin/activate
$> cd deiis
$> python setup.py install
$> cd -
```

## Start RabbitMQ

The RabbitMQ server is available as a Docker image so no installation or setup is required.  We can simply launch the container and start using the server.

```
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management
```

Once the RabbitMQ server has started you can login to its management console at http://localhost:15672 (username: *guest*, password: *guest*). We won't be using the RabbitMQ management console, but it is useful to check if your services are connected to the server and watch how many messages are flowing through the server.

<a name='rabbit-ip'></a>
### Get The IP Address of RabbitMQ

Services running on the same machine as the RabbitMQ server can access the server via *localhost*.  However, services running inside Docker containers are **not** on the *same machine* as the RabbitMQ server.  That is, for services running in a Docker container *localhost* is the Docker container, not the machine running the Docker container.  Therefore we need to know what IP address Docker has assigned to the RabbitMQ server.  Services running in Docker will be able to access RabbitMQ via this IP address.

To view information about the network that Docker has created use the `docker network inspect` command:

```
docker network inspect bridge
```

Look for the *Containers* section in the displayed JSON which contains information about each running container.  In particular we need to make a note of the *IPv4Address* assigned to our *rabbit* container.

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

Here we can see that Docker has assigned the IP address 172.17.0.2 to my RabbitMQ server.  This is the IP address that services running in a Docker container will use to access the RabbitMQ server.  We will store the IP address in an environment variable that the `start.sh` script will pass to to the Docker containers.

```
export RABBIT_HOST=172.17.0.2
```


## Project Layout

Each service lives in its own directory and all services contain the following files:

* **Dockerfile**<br/>
Copies all *.py files to /root and then sets the ENTRYPOINT to call the service.py script.
* **Makefile**<br/>
Defines goals for building and running the Docker container.
* **service.py**<br/>
Start up script used to launch the service.  This is the entrypoint for Docker containers or it can be invoked from the command line.
* **ServiceN.py**<br/>
The service implementation.

The *Dockerfile*, *Makefile*, and *service.py* files are almost identical across all projects.

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

The `-v /tmp:/var/log` parameter used when starting the tutorial/printer container mounts the `/tmp` directory on the machine running Docker as `/var/log` in the Docker container.

A Bash script is also provided that starts all of the containers.

```
$> ./start.sh
```

### Running A Pipeline

The `pipeline.py` script creates a [Message](https://github.com/CMU-11-791/Docker-Tutorial/blob/master/deiis/deiis/rabbit.py#L33) object with the list of parameters as the *route* (list of services) the message will be sent to.
```
python pipeline.py one two three two one one three print
```

### Stopping The Services


The easiest way to stop all the services is to simply kill the Docker containers.  However, the problem with this is that the containers/services are not shutdown cleanly and a service may be terminated before it has finished processing all of its messages.

The correct way to terminate a service is to send it a *poison pill*, which is just a known message that services listen for to indicate they are to stop processing messages and terminate.  Use the `stop.s` script to send the poison pill to all services:

```
$> ./stop.sh
```

To stop individual services use the *stop.py* script and specify just the message queues that the poison pill should be sent to:

```
$> ./stop.py one printer
```

**Note:** The `stop.sh` script simply calls `stop.py` and then removes the Docker containers.
