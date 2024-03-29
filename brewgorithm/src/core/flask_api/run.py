import logging
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_prometheus import monitor
from flask_cors import CORS
from brewgorithm.src.neural import beer2vec, beer_emb, recommender


app = FlaskAPI(__name__)
cors = CORS(app)

beers_map = {}

@app.route("/_health", methods=['GET'])
def healthcheck():
  """healthcheck - hits model with known id"""
  ratebeer_id = 1267
  if int(ratebeer_id) not in beers_map:
    response = jsonify({'response': None,
        'error': "ratebeer_id " + ratebeer_id + " not found"})
    response.status_code = 500
    return response
  beer = beers_map[int(ratebeer_id)]
  descriptors = [x[0] for x in beer_emb.most_similar(positive=[beer['vector']])]
  unique_descriptors = beer_emb.remove_duplicates(descriptors)
  return jsonify({
    'response': {
      'descriptors': unique_descriptors
    }
  })

@app.route("/descriptors/<ratebeer_id>", methods=['GET'])
@app.route("/model/descriptors/<ratebeer_id>", methods=['GET'])
def get_descriptors(ratebeer_id):
  """For a text query, pipe it through the gate and return the best answer."""
  if int(ratebeer_id) not in beers_map:
    response = jsonify({'response': None,
        'error': "ratebeer_id " + ratebeer_id + " not found"})
    response.status_code = 500
    return response
  beer = beers_map[int(ratebeer_id)]
  descriptors = [x[0] for x in beer_emb.most_similar(positive=[beer['vector']])]
  unique_descriptors = beer_emb.remove_duplicates(descriptors)
  return jsonify({
    'descriptors': unique_descriptors,
    'response': {
      'descriptors': unique_descriptors
    }
  })


@app.route("/recommend", methods=['POST'])
@app.route("/model/recommend", methods=['POST'])
def get_recommendations():
  """For a text query, pipe it through the gate and return the best answer."""
  content = request.json
  try:
    assert('ids' in content)
    assert(len(content['ids']) > 0)
    logging.info("/recommend - IDs: " + " ".join(content['ids']));
    return jsonify({'response': recommender.similar_beers([
        int(x) for x in content['ids']], beers_map, beer_emb.EMB_DIM)})
  except (KeyError, AssertionError):
    response = jsonify({'response': None})
    response.status_code = 500
    return response

@app.route("/recommend_subset", methods=['POST'])
@app.route("/model/recommend_subset", methods=['POST'])
def get_subset_recommendations():
  """For a text query, pipe it through the gate and return the best answer."""
  content = request.json
  try:
    assert('ids' in content)
    assert('subset' in content)
    assert(len(content['ids']) > 0)
    logging.info("/recommend_subset - IDs: " + " ".join(content['ids'])  + " Subset: " + " ".join(content['subset']));
    return jsonify({'response': recommender.similar_beers([
        int(x) for x in content['ids']], beers_map, beer_emb.EMB_DIM, subset=[int(x) for x in content['subset']])})
  except (KeyError, AssertionError):
    response = jsonify({'response': None})
    response.status_code = 500
    return response

if __name__ == "__main__":
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  monitor(app, port=8000)
  app.run(host='0.0.0.0', port=5000)

