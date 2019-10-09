#!/bin/bash

gunicorn -b 0.0.0.0 wsgi --worker-class=gevent --workers=4