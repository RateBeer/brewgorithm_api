import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def similar_beers(beer_ids, beers_map, emb_dim, subset=None):
  profile = np.zeros(emb_dim, dtype=np.float32)

  for beer_id in beer_ids:
    if beer_id not in beers_map:
      continue
    profile += beers_map[int(beer_id)]['vector']
  if not np.any(profile):
    raise KeyError

  def __scorer(key_val_pair):
    if key_val_pair[1]['BeerID'] in beer_ids:
      return 0
    return cosine_similarity([profile], [key_val_pair[1]['vector']])[0][0]

  best_matches = []
  if subset is None:
    for key_val_pair in sorted(beers_map.items(), key=__scorer,
                               reverse=True)[:6]:
      best_matches.append((key_val_pair[0], __scorer(key_val_pair)))
  else:
    matched = 0
    for key_val_pair in sorted(beers_map.items(), key=__scorer,
                               reverse=True):
      if key_val_pair[0] in subset:
        best_matches.append((key_val_pair[0], __scorer(key_val_pair)))
        matched += 1
      if matched > 6:
        break

  return best_matches

