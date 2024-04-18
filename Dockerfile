FROM python:3.10
RUN apt-get update \
    && apt-get -y install libpq-dev gcc uvicorn vim \
    && pip install psycopg2 

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app  /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 5000