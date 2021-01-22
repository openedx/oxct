from python:3.8-alpine

# System dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create user
RUN adduser -h /oxct -u 1000 -D oxct oxct
USER oxct

# Build virtualenv
RUN python -m venv /oxct/venv
ENV PATH /oxct/venv/bin:${PATH}
COPY --chown=oxct:oxct ./requirements/base.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy code
COPY --chown=oxct:oxct . /oxct/src
WORKDIR /oxct/src
RUN pip install -e .

# Persist data
ENV OXCT_ROOT /oxct/data
VOLUME /oxct/data

CMD uwsgi --http 0.0.0.0:5000 --module oxct.server.main:app
