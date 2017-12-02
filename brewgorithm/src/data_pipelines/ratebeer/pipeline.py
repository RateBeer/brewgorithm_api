import os
import pymssql
import pickle
from ..config import SQL_SERVER, MODEL_DIR, DATABASE
from ...utils import language

filter_nulls = language.cleaning.filter_nulls

def get_sql_credentials():
  sql_usr = open("/run/secrets/" + os.environ["RATEBEER_DB_USERNAME"]).read().strip()
  sql_pass = open("/run/secrets/" + os.environ["RATEBEER_DB_PASSWORD"]).read().strip()
  return sql_usr, sql_pass

def fetch_beer(beer_id, beer_features=[]):
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252")
  cursor = conn.cursor(as_dict=True)
  cursor.execute("""
      select * from Beer
      where BeerId = %s
  """ % (beer_id, ))
  row = cursor.fetchone()
  if not row:
    raise KeyError

  beer_data = {}
  for field in beer_features:
    beer_data[field] = filter_nulls(row[field])
  return beer_data


def fetch_beer_reviews(beer_id, review_features=[]):
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252")
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


def fetch_beer_ids():
  SQL_USR, SQL_PASS = get_sql_credentials()
  conn = pymssql.connect(SQL_SERVER, SQL_USR, SQL_PASS, DATABASE, charset="CP1252")
  cursor = conn.cursor(as_dict=True)
  cursor.execute("""
      select BeerID from Beer order by Beer.RateCount DESC
  """)
  while True:
    try:
      row = cursor.fetchone()
    except UnicodeDecodeError:
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

