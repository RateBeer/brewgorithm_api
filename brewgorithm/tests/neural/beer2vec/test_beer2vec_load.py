from brewgorithm.src.neural import beer2vec, beer_emb, word_weighter
import numpy as np
import unittest
from sklearn.metrics.pairwise import cosine_similarity


class TestBeer2vec(unittest.TestCase):
  def test_most_similar_test(self):
    beers = beer2vec.get_beer2vec()

    embeddings = beer_emb.embed_doc("apricot peach fruity", word_weighter.is_beer_related)
    emb = np.average(embeddings, axis=0)
    sims = cosine_similarity([emb], [beer['vector'] for beer in beers]).reshape(-1)

    candidates = []
    for i, sim in enumerate(sims):
      candidates.append((sim, i))
    result = [x for x in sorted(candidates, key=lambda i: i[0], reverse=True)[:2]][1]
    self.assertEqual(bool(beers[result[1]]['BeerNamePlain'].strip()), True)
    self.assertEqual(bool(float(beers[result[1]]['Alcohol'])), True)
    self.assertEqual(bool(int(beers[result[1]]['OverallPctl'])), True)
    desc = [a[0] for a in beer_emb.most_similar(positive=[beers[result[1]]['vector']], negative=[])]
    self.assertIn("fruity", desc)


if __name__ == '__main__':
  unittest.main()
