FROM python:3
WORKDIR /app
RUN pip install flask
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

CMD [ "python3", "/app/Achievement2.py" ]
