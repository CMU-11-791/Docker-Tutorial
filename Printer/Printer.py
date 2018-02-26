from deiis.rabbit import Task

import logging
logging.basicConfig()


class Printer(Task):

    def __init__(self, host='localhost'):
        super(Printer, self).__init__('print', host=host)

    def perform(self, message):
        self.logger.info('Printing message')
        fp = open("/var/log/deiis-tutorial.log", 'a')
        fp.write(message)
        fp.write('\n')
        fp.close()
        self.logger.debug('Message printed.')



