from flask import request, jsonify
from flask.ext.api import FlaskAPI
from flask_cors import CORS
from ...neural import beer2vec, beer_emb


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
  return jsonify({'response': beer_emb.most_similar(positive=[beer['vector']])})


if __name__ == "__main__":
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  app.run(host='0.0.0.0')

