FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api.py .

CMD [ "python3", "./api.py" ]