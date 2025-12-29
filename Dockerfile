FROM python:3.10-slim

RUN apt-get update && \
    apt-get -qq -y install tesseract-ocr 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

COPY . .

CMD ["gunicorn","app:app"]
