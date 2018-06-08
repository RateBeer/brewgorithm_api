import os
from ...utils import common

MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../../models/"
MODEL_NAME = "ratebeer.model"

REVIEWS_CAP = 1000
REVIEWS_FLOOR = 300

BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]
