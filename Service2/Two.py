from deiis.rabbit import Task

class Two(Task):
    def __init__(self, host='localhost'):
        super(Two, self).__init__('two', host=host)

    def perform(self, message):
        print 'processing message'
        return message + '\n' + 'service two'
