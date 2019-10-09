#!/bin/bash

gunicorn -b 0.0.0.0:8080 wsgi --reload --worker-class=gevent --workers=4