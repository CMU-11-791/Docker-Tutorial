from deiis.rabbit import Task

class Service3(Task):
    def __init__(self, host='localhost'):
        super(Service3, self).__init__('three', host=host)

    def perform(self, message):
        self.logger.info('processing message')
        return message + '\n' + 'service three'
