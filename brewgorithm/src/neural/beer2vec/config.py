import os

MODEL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../../../models/"
MODEL_NAME = "ratebeer.model"

TRAINING_CAP = 6000  # maximum number of beers to train at once
REVIEWS_CAP = 1000  # maximum number of reviews incorporated into Brewgorithm training
REVIEWS_FLOOR = 300  # minimum number of reviews required for beer to be incorporated into Brewgorithm

BEER_FIELDS = ["BeerID", "BeerNamePlain", "BeerStyleID", "Alcohol", "AverageRating", "OverallPctl"]
