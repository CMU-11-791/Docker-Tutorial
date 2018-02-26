#!/usr/bin/env bash

if [ "$RABBIT_HOST" = "" ] ; then
    RABBIT_HOST=172.17.0.2
fi

for name in one two three ; do
	docker run -d -e HOST=$RABBIT_HOST --name $name tutorial/$name 
done

docker run -d -e HOST=$RABBIT_HOST --name printer -v /tmp:/var/log tutorial/printer


