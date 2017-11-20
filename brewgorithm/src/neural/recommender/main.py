import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def similar_beers(beer_ids, beers_map, emb_dim):
  profile = np.zeros(emb_dim, dtype=np.float32)

  for beer_id in beer_ids:
    if beer_id not in beers_map:
      raise KeyError
    profile += beers_map[int(beer_id)]['vector']

  def __scorer(key_val_pair):
    if key_val_pair[1]['BeerID'] in beer_ids:
      return 0
    return cosine_similarity([profile], [key_val_pair[1]['vector']])[0][0]

  best_matches = []
  for key_val_pair in sorted(beers_map.items(), key=__scorer,
                             reverse=True)[:6]:
    best_matches.append((key_val_pair[0], __scorer(key_val_pair)))

  return best_matches

