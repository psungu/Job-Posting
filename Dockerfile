# FROM python:3.9-slim
# WORKDIR /
# COPY ./requirements.txt requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY ./app.py app
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]


FROM condaforge/mambaforge AS build

COPY environment.yml .

RUN mamba env create -f environment.yml

RUN conda install -c conda-forge conda-pack
# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n search-service -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# When image is run, run the code with the environment
# activated:
WORKDIR /search-service

COPY ./src /search-service/src

SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && uvicorn src.app:app --host 0.0.0.0 --port 19530
