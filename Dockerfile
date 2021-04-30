FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /usr/src
COPY ./api /usr/src/api

RUN python3 -m pip install -r api/requirements.txt