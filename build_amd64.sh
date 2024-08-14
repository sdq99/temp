#!/bin/bash

docker buildx build --platform linux/amd64 -t ddd:latest . && docker run --platform linux/amd64 ddd:latest
