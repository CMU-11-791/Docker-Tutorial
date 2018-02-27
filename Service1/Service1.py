from deiis.rabbit import Task

class Service1(Task):
    def __init__(self, host='localhost'):
        super(Service1, self).__init__('one', host=host)

    def perform(self, message):
        print 'processing message'
        return message + '\n' + 'service one'
