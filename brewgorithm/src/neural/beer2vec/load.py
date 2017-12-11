import pickle
from pathlib import Path
from .config import MODEL_DIR, MODEL_NAME, MODEL_URL
from ...utils.network.download import download_file

if not Path(MODEL_DIR + MODEL_NAME).is_file():
  beer_labels = None
else:
  beer_labels = pickle.load(open(MODEL_DIR + MODEL_NAME, "rb"))


def get_beer2vec():
  if beer_labels is None:
    raise Exception("No installed beer2vec models.")
  return beer_labels

def refresh_beer2vec_model():
  download_file(MODEL_URL, MODEL_DIR + MODEL_NAME)
  beer_labels = pickle.load(open(MODEL_DIR + MODEL_NAME, "rb"))

