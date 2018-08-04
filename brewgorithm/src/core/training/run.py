from brewgorithm.src.neural import beer2vec

if __name__ == '__main__':

    """For an array of ids , train the selected beer ids and return success / fail."""
    content = ["2512"]
    try:
        assert (len(content) > 0)

        try:
            beer2vec.dev.train.gen_beer2vec(beer2vec.config.MODEL_NAME,
                                            [int(x) for x in content], should_overwrite=True)
            print("Success")
        except KeyError as e:
            print("Failure - Beer Id not found in DB: {}".format(e))
        except AssertionError as e:
            print("Failure - Not enough reviews to train for beer: {}".format(e))
        except Exception as e:
            print("Training crashed: {}".format(e))

    except (KeyError, AssertionError):
        print("Error retrieving data")
