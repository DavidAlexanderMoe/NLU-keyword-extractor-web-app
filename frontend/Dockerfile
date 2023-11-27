FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 3000/tcp

ENTRYPOINT ["python","main.py"]