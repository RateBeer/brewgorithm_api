import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def getFromEnvironment(key):
  try:
      return os.environ[key]
  except Exception as e:
    logging.error('No enviroment key found for: ' + key)
