from weather import *
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--http')
    (options, args) = parser.parse_args()