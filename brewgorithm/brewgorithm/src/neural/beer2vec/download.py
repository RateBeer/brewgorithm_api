from . import config
from ...utils.network.download import download_file


if __name__ == "__main__":
  download_file(config.MODEL_URL, config.MODEL_DIR + config.MODEL_NAME)

