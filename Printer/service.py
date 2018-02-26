import os, sys
from Printer import Printer

if __name__ == '__main__':
    host = os.environ.get('HOST', 'localhost')
    if len(sys.argv) > 1:
        if sys.argv[1] != '/bin/bash':
            host = sys.argv[1]

    print "Host is " + host
    service = Printer(host=host)
    print('Staring ' + service.__class__.__name__)
    service.start()

    print('Waiting for ' + service.__class__.__name__)
    service.join()

    print('Done.')
