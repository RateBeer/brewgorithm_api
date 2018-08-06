import os
from ...utils import common

MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../../models/"
MODEL_NAME = "ratebeer.model"

TRAINING_CAP = 3500
REVIEWS_CAP = 1000
REVIEWS_FLOOR = 300
RATING_FLOOR = 3.4

BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]
