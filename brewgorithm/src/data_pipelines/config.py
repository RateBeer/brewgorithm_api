import os
from ..utils import common

SQL_SERVER = common.tools.getFromEnvironment('RATEBEER_DB_HOST')
SQL_PORT = common.tools.getFromEnvironment('RATEBEER_DB_PORT')
DATABASE = common.tools.getFromEnvironment('RATEBEER_DB_DATABASE')
MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/storage/"
