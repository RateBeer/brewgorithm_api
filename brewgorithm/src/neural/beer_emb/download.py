from . import config
from ...utils.network.download import download_file


if __name__ == "__main__":
  download_file(config.SMALL_URL, config.MODEL_DIR + config.SMALL_NAME)
  download_file(config.MID_URL, config.MODEL_DIR + config.MID_NAME)
  download_file(config.LARGE_URL, config.MODEL_DIR + config.LARGE_NAME)
  download_file(config.X_LARGE_URL, config.MODEL_DIR + config.X_LARGE_NAME)

