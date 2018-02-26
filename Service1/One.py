from deiis.rabbit import Task

class One(Task):
    def __init__(self, host='localhost'):
        super(One, self).__init__('one', host=host)

    def perform(self, message):
        print 'processing message'
        return message + '\n' + 'service one'
