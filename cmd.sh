#!/bin/bash

gunicorn -b 0.0.0.0:8001 wsgi --worker-class=gevent --workers=4
