import logging
import sys
import numpy as np

from ..access_ext import beer_emb
from ..access_ext import word_weighter
from ..access_ext import data_pipelines
from .. import config

pipeline = data_pipelines.ratebeer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def encode(embeddings):
  if np.linalg.norm(embeddings) == 0:
    return np.zeros(beer_emb.EMB_DIM)
  return np.average(embeddings, axis=0) / np.linalg.norm(embeddings)


def gen_beer_vectors(beer_ids, label_features=["BeerNamePlain", "ABV"]):
  '''
  Generate Ratebeer data with natural language included as an encoded setup
  '''
  logging.debug('gen_beer_vectors')
  for beer_id in beer_ids:
    beer_vec = np.zeros(beer_emb.EMB_DIM, dtype=np.float64)
    try:
      labels = pipeline.fetch_beer(beer_id, label_features)
    except KeyError:
      raise KeyError(beer_id)
    except UnicodeDecodeError:
      continue
    i = 0
    for review_features, text in pipeline.fetch_beer_reviews(beer_id):
      try:
        beer_vec = beer_vec + encode(beer_emb.embed_doc(text, word_weighter.is_beer_related))
        i += 1
        if config.REVIEWS_CAP is not False:
          if i > config.REVIEWS_CAP:
            break
      except AssertionError:
        continue

    # instead of raising an error, prevent the model
    # from being updated instead (by setting beer_vec to zeros
    # which will be caught in train.py)
    # assert(i >= config.REVIEWS_FLOOR), beer_id

    if i >= config.REVIEWS_FLOOR:
      beer_vec = np.zeros(beer_emb.EMB_DIM, dtype=np.float64)

    beer_vec = beer_vec / np.linalg.norm(beer_vec)
    labels['vector'] = beer_vec
    yield labels

