From tensorflow/tensorflow:latest-py3

# Install apk packages
RUN apt update \
  && apt install gcc make libc-dev g++ bzip2 git libssl-dev openssl build-essential -y

# Establish working directory
WORKDIR /service 

# Copying pip requirement files 
COPY requirements.txt requirements.txt

# Install python dependencies
RUN export C_INCLUDE_PATH=/usr/include
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

# Download natural language models
RUN python -m spacy download en

# Install dev-only dependencies
RUN pip3 install pytest

COPY ./brewgorithm ./brewgorithm

ENV WRITE_API 1

RUN mkdir -p /service/brewgorithm/src/neural/beer2vec/models/
RUN mkdir -p /service/brewgorithm/src/neural/beer_emb/models/

# Download beer models
RUN python3 -m brewgorithm.src.neural.beer2vec.download
RUN python3 -m brewgorithm.src.neural.beer_emb.download

# Run tests
RUN py.test brewgorithm/tests
CMD python3 -m brewgorithm.src.core.flask_api.run
