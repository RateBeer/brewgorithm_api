import os
MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/models/"
MODEL_NAME = "ratebeer.model"
MODEL_URL = "https://s3.amazonaws.com/brewgorithm-models/17-11-20/ratebeer.model"

REVIEWS_CAP = 1000
REVIEWS_FLOOR = 300

BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]

AWS_ACCESS_KEY_ID = '[your access key id]'
AWS_SECRET_ACCESS_KEY = '[your secret access key here]'
S3_BUCKET = 'brewgorithm-models' 
S3_PATH = '17-11-20/'
