#!/bin/sh

set -e

docker build --platform=linux/amd64 -f environment/Dockerfile -t ghcr.io/benjamin-heasly/geffenlab-openephys-events:local .

docker run --rm ghcr.io/benjamin-heasly/geffenlab-openephys-events:local conda_run python /opt/code/run.py
