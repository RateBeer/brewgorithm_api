# from multiprocessing import Pool
import logging
import sys
import os
import pickle
import numpy as np
import boto
from boto.s3.key import Key

from .. import config
from .preprocessing import gen_beer_vectors
from ..access_ext import data_pipelines

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def gen_ids(number):
  beer_ids = []
  i = 0
  for beer_id in data_pipelines.ratebeer.fetch_beer_ids():
    beer_ids.append(beer_id)
    i += 1
    if i > number:
      break
  return beer_ids


def gen_beer2vec(model_name, beer_ids, should_overwrite=False):

  # if should_overwrite: trains all beers in beer_ids and overwrites over copies
  # else: trains only the  unseen beers in beer_ids
  # Attempt to load in initial beers
  
  # remove duplicate beer ids
  beer_ids = list(set(beer_ids))

  try:
    logging.info("Running gen_beer2vec")
    beer_labels = pickle.load(open(config.MODEL_DIR + model_name, "rb"))

    if should_overwrite:
      unchanged_beer_labels = []
      input_beer_ids = set(beer_ids)
      for beer in beer_labels:
        if beer['BeerID'] not in input_beer_ids:
          unchanged_beer_labels.append(beer)
        else:
          logging.debug("Overwriting " + beer['BeerNamePlain'])
      beer_labels = unchanged_beer_labels

    else:
      input_beer_ids = set(beer_ids)
      for beer in beer_labels:
        if beer['BeerID'] in input_beer_ids:
          logging.debug("Skipping " + beer['BeerNamePlain'])
          input_beer_ids.remove(beer['BeerID'])
      beer_ids = list(input_beer_ids)

    logging.debug(str(len(beer_labels)) + " initial beers")
  except (OSError, IOError) as e:
    beer_labels = []
    logging.debug("0 initial beers")

  for y in gen_beer_vectors(beer_ids=beer_ids, label_features=config.BEER_FIELDS):
    try:
      if y['sufficient_data'] == False:
        logging.debug("Insufficient data for " + \
          y['BeerNamePlain'].encode('ascii', 'ignore').decode('ascii', 'ignore'))
        continue
      # If not valid
      if np.isnan(np.sum(y['vector'])):
        logging.debug("Nan Error")
        continue

      # Must be valid
      logging.debug("Saving " + \
        y['BeerNamePlain'].encode('ascii', 'ignore').decode('ascii', 'ignore'))
      beer_labels.append(y)

    except UnicodeEncodeError:
      logging.debug("Unicode Error")
      continue

  pickle.dump(beer_labels, open(config.MODEL_DIR + model_name, 'wb'))
  save_beer2vec_s3(model_name)
  
  return beer_labels

def save_beer2vec_s3(model_name):
  '''Uploads the beer2vec model file to s3, overwriting the existing model'''
  logging.debug("Attempting to upload to s3")
  aws_access_key_id = open("/run/secrets/" + os.environ["AWS_ID_SECRET"]).read().strip()
  aws_secret_access_key = open("/run/secrets/" + os.environ["AWS_KEY_SECRET"]).read().strip()

  conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
  logging.debug("Connected to s3")
  brewgorithm_bucket = conn.get_bucket(config.S3_BUCKET)
  s3_file = Key(brewgorithm_bucket)
  s3_file.key = config.S3_PATH + model_name
  s3_file.set_contents_from_filename(config.MODEL_DIR + model_name, replace=True)
  s3_file.set_acl('public-read')

  logging.debug("s3 file written")

  return True

if __name__ == "__main__":
  beer_labels = gen_beer2vec(config.MODEL_NAME, gen_ids(20000))
  logging.debug("Training complete")
