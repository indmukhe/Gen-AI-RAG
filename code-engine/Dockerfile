FROM python:3.11-slim

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./db /code/db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
