from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
from ...neural import beer2vec, beer_emb, recommender


app = FlaskAPI(__name__)
cors = CORS(app)

beers_map = {}


@app.route("/descriptors/<ratebeer_id>", methods=['GET'])
def get_descriptors(ratebeer_id):
  """For a text query, pipe it through the gate and return the best answer."""
  if int(ratebeer_id) not in beers_map:
    return jsonify({'response': None, 'statusCode': 500,
        'error': "ratebeer_id " + ratebeer_id + " not found"})
  beer = beers_map[int(ratebeer_id)]
  descriptors = [x[0] for x in beer_emb.most_similar(positive=[beer['vector']])]
  unique_descriptors = beer_emb.remove_duplicates(descriptors)
  return jsonify({'descriptors': unique_descriptors, 'statusCode': 200})


@app.route("/recommend", methods=['POST'])
def get_recommendations():
  """For a text query, pipe it through the gate and return the best answer."""
  content = request.json
  try:
    assert('ids' in content)
    assert(len(content['ids']) > 0)
    return jsonify({'statusCode': 200, 'response': recommender.similar_beers([
        int(x) for x in content['ids']], beers_map, beer_emb.EMB_DIM)})
  except (KeyError, AssertionError):
    return jsonify({'response': None, 'statusCode': 500})

@app.route("/update_vectors", methods=['POST'])
def update_vectors():
  """For a json array, train the selected beer ids and return success / fail."""
  content = request.json
  try:
    assert('ids' in content)
    assert(len(content['ids']) > 0)

    try:
      beer2vec.dev.train.gen_beer2vec(beer2vec.config.MODEL_NAME,
          [int(x) for x in content['ids']], should_overwrite=True)
      return jsonify({'statusCode': 200, 'status': "success"})
    except AssertionError as e:
      return jsonify({'statusCode': 500, 'status': 'failure', 'error': 
          "not enough reviews to train for beer: {}".format(e)})
    except Exception as e:
      return jsonify({'statusCode': 500, 'status': 'failure', 'error': 
          "training crashed"})

  except (KeyError, AssertionError):
    return jsonify({'response': None, 'statusCode': 500})

if __name__ == "__main__":
  beers = beer2vec.get_beer2vec()
  for beer in beers:
    beers_map[int(beer['BeerID'])] = beer
  app.run(host='0.0.0.0', port=5000)

