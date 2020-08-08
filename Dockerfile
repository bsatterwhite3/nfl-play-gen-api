FROM python:3.7-slim

EXPOSE 5000

WORKDIR /usr/src/app

RUN mkdir app
RUN mkdir cache

COPY requirements.txt ./
COPY playgen ./playgen/
COPY app.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./app.py" ]
