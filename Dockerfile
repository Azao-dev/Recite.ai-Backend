FROM python:3.10-slim-bullseye

RUN apt-get update && \
    apt-get -qq -y install --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
