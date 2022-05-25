#!/usr/bin/env python
#------------------------------------------------------------------------
# runserver.py
# Authors: Nsomma Alilonu
#------------------------------------------------------------------------
import argparse
from sys import argv, exit, stderr
from paths import app

def main(argv):
    try: 
        parser = argparse.ArgumentParser(description='Darthouse application', allow_abbrev=False)
        parser.add_argument('port', type = int,  nargs = 1, help='the port at which the server should listen')

        args = parser.parse_args()

        port = int(args.port[0])

    except Exception as e:
        print(e, file=stderr)

    app.run(host='0.0.0.0', port=port, debug=True)

#------------------------------------------------------------------------
if __name__ == '__main__':
    main(argv)