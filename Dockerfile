FROM python:3.7.0-slim
WORKDIR /honeybadger
ADD honeybadger honeybadger
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
ADD wsgi.py wsgi.py
RUN pip install pipenv && pipenv install --system
ADD cmd.sh cmd.sh
RUN chmod +x cmd.sh
ENTRYPOINT [ "/honeybadger/cmd.sh" ]

