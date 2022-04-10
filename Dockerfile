FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirement.txt

CMD ["python", "app/main.py"]