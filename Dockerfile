FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8080

WORKDIR /code


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /code/
RUN chmod +x  /code/entrypoint.sh

COPY src/ /code

ENTRYPOINT ["sh", "-c", "chmod +x /code/entrypoint.sh && /code/entrypoint.sh"]
