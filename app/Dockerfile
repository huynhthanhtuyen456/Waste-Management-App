FROM python:3.9

LABEL maintainer="Tuyen Huynh <tuyenhtgcs220307@fpt.edu.vn>"
LABEL app="Task Service"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . /app


CMD ["fastapi", "run", "main.py", "--port", "8000", "--workers", "3"]