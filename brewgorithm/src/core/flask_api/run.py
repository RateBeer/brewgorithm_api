from flask import request, jsonify
from flask.ext.api import FlaskAPI
from flask_cors import CORS
from ...neural import beer2vec, beer_emb, recommender


app = FlaskAPI(__name__)
cors = CORS(app)

beers_map = {}


@app.route("/descriptor", methods=['POST'])
def get_descriptor():
  """For a text query, pipe it through the gate and return the best answer."""
  ratebeer_id = int(request.data.get('id', ''))
  if ratebeer_id not in beers_map:
    return jsonify({'response': None})
  beer = beers_map[ratebeer_id]
  descriptors = [x[0] for x in beer_emb.most_similar(positive=[beer['vector']])]
  unique_descriptors = beer_emb.remove_duplicates(descriptors)
  return jsonify({'response': unique_descriptors})


@app.route("/recommend", methods=['POST'])
def get_recommendations():
  """For a text query, pipe it through the gate and return the best answer."""
  content = request.json

  try:
    assert('ids' in content)
    assert(len(content['ids']) > 0)
    return jsonify({'response': recommender.similar_beers([
        int(x) for x in content['ids']], beers_map, beer_emb.EMB_DIM)})
  except (KeyError, AssertionError):
    return jsonify({'response': None})


if __name__ == "__main__":
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  app.run(host='0.0.0.0', port=5000)

