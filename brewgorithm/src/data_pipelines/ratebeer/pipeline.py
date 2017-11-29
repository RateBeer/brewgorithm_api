import pymssql
import pickle
from ..config import SQL_SERVER, SQL_USR, SQL_PASS, MODEL_DIR, DATABASE
from ...utils import language

filter_nulls = language.cleaning.filter_nulls

def fetch_beer(beer_id, beer_features=[]):
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

