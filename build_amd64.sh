#!/bin/bash

docker buildx build --platform linux/amd64 -t d . && docker run --platform linux/amd64 d
