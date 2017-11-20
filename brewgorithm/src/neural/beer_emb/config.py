import os

MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/models/"

SMALL_NAME = "server64.model"
MID_NAME = "server128.model"
LARGE_NAME = "server256.model"
X_LARGE_NAME = "server512.model"
MODEL_NAME = X_LARGE_NAME

SMALL_URL = "https://d3t9movkb8ddzf.cloudfront.net/17-11-20/server64.model"
MID_URL = "https://d3t9movkb8ddzf.cloudfront.net/17-11-20/server128.model"
LARGE_URL = "https://d3t9movkb8ddzf.cloudfront.net/17-11-20/server256.model"
X_LARGE_URL = "https://d3t9movkb8ddzf.cloudfront.net/17-11-20/server512.model"

EMB_DIM = 512
