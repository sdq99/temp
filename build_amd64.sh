#!/bin/bash

docker build  -t phpmyadmin . && docker run -d phpmyadmin
