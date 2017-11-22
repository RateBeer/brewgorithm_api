import os
MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/models/"
MODEL_NAME = "ratebeer.model"
MODEL_URL = "https://d3t9movkb8ddzf.cloudfront.net/17-11-20/ratebeer.model"

REVIEWS_CAP = 3000
REVIEWS_FLOOR = 300
BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]
