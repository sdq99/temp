#!/bin/bash

docker buildx build  -t mindmaze:latest . && docker run mindmaze:latest
