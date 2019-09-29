#!/bin/bash

gunicorn wsgi --reload --worker-class=gevent --workers=4