from gensim.models import Word2Vec
from pathlib import Path
import numpy as np
import editdistance
from .config import MODEL_NAME, MODEL_DIR, EMB_DIM
from ...utils import language

clean_word = language.cleaning.clean_word
parsing = language.parsing

### ADD TRADEMARKS HERE
### ex: = ["budweiser", "abi"]
trademarks = ["budweiser"]


if not Path(MODEL_DIR + MODEL_NAME).is_file():
  model = None
else:
  model = Word2Vec.load(MODEL_DIR + MODEL_NAME)


def remove_duplicates(words):
  """Remove duplicates from descriptor list

  Duplicates are within two levenshtein edit distances away from each other,
  or they are only different in capitalization.
  Duplicates that end in y are preferred. Other optimizations
  not yet implemented.

  Examples:
    Input: [space, spacey, spaceys]
    Output: [spacey]

    Input: [guiness, guinness, guinnesses]
    Output: [guiness, guinnesses]
    This is non-ideal, but will require more time to fix

    Input: [abc, abcde, abcfg, efgh]
    Output: [abc, efgh]
    This is non-ideal, because output depends on order of input

  Return:
    unique list -- desciptor list without duplicates
  """

  unique_words = set()
  for word in words:
    is_unique = True
    words_to_remove = []
    for unique_word in unique_words:
      if editdistance.eval(word.lower(), unique_word.lower()) <= 2:
        if word[-1].lower() == 'y' and unique_word[-1].lower() != 'y':
          words_to_remove.append(unique_word)
        else:
          is_unique = False
    if is_unique:
      unique_words.add(word)
      for word_to_remove in words_to_remove:
        unique_words.remove(word_to_remove)

  return sorted([word for word in unique_words if word not in trademarks], key=lambda x: words.index(x))


def most_similar(positive=None, negative=None):
  """Return most similar words as described by positive and negative words.

  Return:
    most_similar_words -- list of tuples (word, similarity_score)
  """
  if model is None:
    raise Exception("No installed word_emb models.")
  if positive is None:
    positive = []
  if negative is None:
    negative = []
  return model.wv.most_similar_cosmul(positive=positive, negative=negative)


def embed_word(word, default=None):
  """Return beer embedding for a word."""
  if model is None:
    raise Exception("No installed word_emb models.")
  if default is None:
    default = np.zeros(EMB_DIM)
  word = clean_word(word)
  if word in model:
    return model.wv[word]
  else:
    return default


def embed_doc(doc_string, word_filter):
  """Given a doc string, parse it and calculate embeddings.

  Return:
    embeddings -- numpy array 2d, (number_of_token_embeddings X EMB_DIM)
  """
  if model is None:
    raise Exception("No installed word_emb models.")
  embeddings = []
  # for each token in the doc string
  for token in parsing.tokenize(doc_string, clean=False):
    word_vector = embed_word(clean_word(token.text))
    # when the word vector is all zeros
    if not word_vector.any():
      continue

    # if there is no word_filter or the word filter is positive
    if not word_filter or word_filter(word_vector):
      embeddings.append(word_vector)
    else:
      continue
  # if no embedding was found for any of the tokens in the doc_string
  if len(embeddings) == 0:
    return np.zeros((1, EMB_DIM))
  return np.array(embeddings)


def get_model():
  """Return the beer embedding model instance."""
  if model is None:
    raise Exception("No installed word_emb models.")
  return model

