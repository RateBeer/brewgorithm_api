from brewgorithm.src.neural import beer2vec, beer_emb, word_weighter
import numpy as np
import unittest
from sklearn.metrics.pairwise import cosine_similarity

config = beer2vec.config
encode = beer2vec.dev.preprocessing.encode


class TestBeer2vecDev(unittest.TestCase):
  def test_preprocessing(self):
    self.assertTrue(np.all(encode(np.zeros(beer_emb.config.EMB_DIM)) == np.zeros(beer_emb.config.EMB_DIM)))
    # self.assertEquals(np.linalg.norm(encode(beer_emb.embed_word("chocolate"))), 1)
  
  """ not doable until we have a test model
  def test_get_beer_vectors(self):
    beers = beer2vec.dev.train.gen_beer2vec('tests/temp_model.p', [48429, 422, 3214])
    self.assertTrue(type(beers) == list)
    self.assertTrue(len(beers) > 0)
    for beer in beers:
      for label in config.BEER_FIELDS:
        assert(label in beer)
    self.assertTrue(cosine_similarity([beers[0]['vector']], [beers[1]['vector']])[0][0] > cosine_similarity([beers[1]['vector']], [beers[2]['vector']])[0][0])
  """

if __name__ == '__main__':
  unittest.main()
