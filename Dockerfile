FROM python:3.9-alpine
WORKDIR /app
RUN apk add --update --no-cache build-base
RUN pip install -U discord.py
COPY . .
CMD ["python", "giraffe/head.py"]