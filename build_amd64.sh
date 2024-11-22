#!/bin/bash

docker build  -t globel-images-new:latest . && docker run -d 0.0.0.0:7000->8080/tcp, :::7000->8080/tcp PhpMyAdmin:latest
