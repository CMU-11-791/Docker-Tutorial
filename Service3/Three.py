from deiis.rabbit import Task

class Three(Task):
    def __init__(self, host='localhost'):
        super(Three, self).__init__('three', host=host)

    def perform(self, message):
        self.logger.info('processing message')
        return message + '\n' + 'service three'
