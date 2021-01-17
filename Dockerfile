FROM python:3.9-alpine
WORKDIR /app
RUN apk add --update --no-cache build-base
COPY requirements.txt ./requirements.txt
RUN pip install -U -r ./requirements.txt
COPY . .
CMD ["python", "giraffe/head.py"]