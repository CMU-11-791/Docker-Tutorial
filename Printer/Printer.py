from deiis.rabbit import Task

import logging
logging.basicConfig(filename='printer.log', level=logging.DEBUG)


class Printer(Task):

    def __init__(self, host='localhost'):
        super(Printer, self).__init__('print', host=host)

    def perform(self, message):
        message = message + '\n' + 'print'
        print message
        fp = open("/var/log/deiis-tutorial.log", 'a')
        fp.write(message)
        fp.write('\n')
        fp.close()
        return message



