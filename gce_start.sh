#!/usr/bin/env bash
docker-machine create -d google \
--google-machine-type f1-micro \
--google-machine-image https://www.googleapis.com/compute/v1/projects/coreos-cloud/global/images/coreos-stable-1185-3-0-v20161101 \
--google-project scalica-hashtag \
machine
