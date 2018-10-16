#!/bin/bash
set -ev

# Run the tests
py.test --cov=./

# Upload results to codecov
codecov -t e71480e0-8297-477f-b479-7c2595a58c88

exit 0;
