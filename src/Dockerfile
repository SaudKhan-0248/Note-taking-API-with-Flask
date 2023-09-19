FROM python:3.11.5-alpine3.17
WORKDIR /src
COPY ./requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src/

EXPOSE 5000

CMD [ "python3", "run.py"]
