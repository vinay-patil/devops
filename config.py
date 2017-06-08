import os
import sys
import logging

logging.basicConfig(stream=sys.stdout)

DEBUG = True

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 1234
REDIS_DB = 0

TEXT_API = 'http://www.randomtext.me/api/gibberish'
