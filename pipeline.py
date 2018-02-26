import sys
from deiis.rabbit import Message, MessageBus

if __name__ == '__main__':
    message = Message(body='start', route=sys.argv[1:])
    bus = MessageBus()
    bus.send(message)
