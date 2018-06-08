import pickle
from pathlib import Path
from .config import MODEL_DIR, MODEL_NAME

if not Path(MODEL_DIR + MODEL_NAME).is_file():
  beer_labels = None
else:
  beer_labels = pickle.load(open(MODEL_DIR + MODEL_NAME, "rb"))


def get_beer2vec():
  if beer_labels is None:
    raise Exception("No installed beer2vec models.")
  return beer_labels
