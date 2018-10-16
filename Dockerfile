From tensorflow/tensorflow:latest-py3

ENV BUILD_CACHE=1-30-8-2018

EXPOSE 8000
EXPOSE 5000

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
RUN pip3 install pytest-cov
RUN pip3 install codecov
RUN pip3 install coverage

COPY ./brewgorithm ./brewgorithm

# Run tests
#RUN py.test brewgorithm/tests
CMD python3 -m brewgorithm.src.core.flask_api.run

HEALTHCHECK --interval=5s \
            --timeout=5s \
            --retries=6 \
            CMD curl -fs http://localhost:5000/_health || exit 1
