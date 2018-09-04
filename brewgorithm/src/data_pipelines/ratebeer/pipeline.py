import logging
import sys
import os
import pymssql
import boto3
from ..config import SQL_SERVER, DATABASE, SQL_PORT
from ...utils import language

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

filter_nulls = language.cleaning.filter_nulls

def getSSMValue(param_name):
    ssm = boto3.client('ssm',
        region_name=os.environ["SSM_AWS_REGION"]
    )

    response = ssm.get_parameters(
        Names=[
            param_name,
        ],
        WithDecryption=True
    )

    return response['Parameters'][0]['Value']

def get_sql_credentials():
  sql_usr = getSSMValue(os.environ["SSM_KEY_RATEBEER_DB_USER"])
  sql_pass = getSSMValue(os.environ["SSM_KEY_RATEBEER_DB_PASS"])
  return sql_usr, sql_pass

def fetch_beer(beer_id, beer_features=[]):
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252", port=SQL_PORT)
  logging.info('connected to db')
  cursor = conn.cursor(as_dict=True)
  cursor.execute("""
      select * from Beer
      where BeerId = %s
  """ % (beer_id,))
  row = cursor.fetchone()
  if not row:
    logging.error('No rows found for query')
    raise KeyError

  beer_data = {}
  for field in beer_features:
    beer_data[field] = filter_nulls(row[field])
  logging.debug(beer_data)

  return beer_data


def fetch_beer_reviews(beer_id, review_features=[]):
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252", port=SQL_PORT)
  cursor = conn.cursor(as_dict=True)
  cursor.execute("""
      select *
      from Beer m
      left join BeerRating
       on m.BeerId = BeerRating.BeerId
       where m.BeerId = %s
      order by m.OverallPctl DESC, BeerRating.BeerId ASC
  """ % (beer_id,))

  while True:
    # Load in row, skip if mssql gives UnicodeDecodeError
    try:
      row = cursor.fetchone()
    except UnicodeDecodeError:
      continue
    if not row:
      break

    # Ignore if missing tag descriptions or comments
    if (not row['Comments']) or (row['Comments'] == " "):
      continue

    review_data = []
    for field in review_features:
      review_data.append(filter_nulls(row[field]))

    yield review_data, row['Comments'].encode('ascii', 'ignore').decode('ascii', 'ignore')


def fetch_beer_ids(reviews_floor):
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252", port=SQL_PORT)
  cursor = conn.cursor(as_dict=True)
  logging.debug('connected to db to fetch beer ids') # get beers that have a minimum number of reviews
  cursor.execute("""
      select BeerID from Beer where BeerID IN 
      (select BeerID from BeerRating group by BeerID having count(*) >= %s)
  """ % (str(reviews_floor),))
  while True:
    try:
      row = cursor.fetchone()
      if row and row['BeerID']:
        logging.info("Fetched Beer ID: " + str (row['BeerID']))
    except UnicodeDecodeError:
      logging.error('UnicodeDecodeError')
      continue
    if not row:
      break
    yield row['BeerID']


def stream_text_corpus():
  '''
  Only yield reviews' raw texts
  '''
  for beer_id in fetch_beer_ids():
    for review_data, text in fetch_beer_reviews(beer_id):
      if text:
        yield text


