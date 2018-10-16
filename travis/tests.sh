#!/bin/bash
set -ev

IMAGE_NAME=brewgorithm-${TRAVIS_BUILD_NUMBER}-test

docker build -t ${IMAGE_NAME} .

docker run ${IMAGE_NAME} /bin/bash -c "py.test --cov=./; codecov -t=${CODECOV_TOKEN}"

exit 0;
