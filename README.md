[![codecov](https://codecov.io/gh/RateBeer/brewgorithm_api/branch/master/graph/badge.svg?token=9LYaPCNblT)](https://codecov.io/gh/RateBeer/brewgorithm_api) [![Build Status](https://travis-ci.com/RateBeer/brewgorithm_api.svg?token=T2ttsRBxCEzfp8zVPhTP&branch=dev)](https://travis-ci.com/RateBeer/brewgorithm_api)

### Requirements

- Docker-CE version 17.09.0-ce
- Docker Compose version 1.14.0

### Getting Started

```
docker-compose up --build
```

### Examples

##### Get a beer's descriptors:

Get request: `$API/descriptors/<ratebeer_id>`
If ID is not valid, you will get back:
`{'response': None, 'statusCode': 500, 'error': "ratebeer_id <ratebeer_id> not found"}`
If it is valid, you will get back:
`{'descriptors': ['<descriptor1>', '<descriptor2>', '<descriptor3>', ...], 'statusCode': 200}

##### Get beer recommendations based off list of beers:

Post request: `$API/recommend`.
JSON body: `{'ids': [<id1>, <id2>...]}`
If any ids are invalid, you will get back:
`{'response': None, 'statusCode': 500}`
If all are valid, you will get back:
({'statusCode': 200, 'response':[<recommended_id1>,<recommended_id2>...]}

##### Get beer recommendations based off list of beers from a subset:

Post request: `$API/recommend_subset`.
JSON body: `{'ids': [<id1>, <id2>...], 'subset': [<e_id1>, <e_id2>...]}`
If any ids are invalid, you will get back:
`{'response': None, 'statusCode': 500}`
If all ids are valid, you will get back:
({'statusCode': 200, 'response':[<recommended_id1>,<recommended_id2>...]}

##### Get beer recommendations based off list of beers from a subset:

Post request: `$API/recommend_subset`.
JSON body: `{'ids': [<id1>, <id2>...], 'subset': [<e_id1>, <e_id2>...]}`
If any ids are invalid, you will get back:
`{'response': None, 'statusCode': 500}`
If all ids are valid, you will get back:
({'statusCode': 200, 'response':[<recommended_id1>,<recommended_id2>...]}

##### Train beers that meet configured # of reviews minimum

python3 brewgorithm/src/neural/beer2vec/dev/train.py
