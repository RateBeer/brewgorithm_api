import os
from ...utils import common

MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/models/"
MODEL_NAME = "ratebeer.model"
MODEL_URL = "https://s3.amazonaws.com/brewgorithm-model/17-11-20/ratebeer.model"

REVIEWS_CAP = 1000
REVIEWS_FLOOR = 300

BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]

S3_BUCKET = common.tools.getFromEnvironment('S3_BUCKET')
S3_PATH = common.tools.getFromEnvironment('S3_PATH')
