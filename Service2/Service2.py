from deiis.rabbit import Task

class Service2(Task):
    def __init__(self, host='localhost'):
        super(Service2, self).__init__('two', host=host)

    def perform(self, message):
        print 'processing message'
        return message + '\n' + 'service two'
