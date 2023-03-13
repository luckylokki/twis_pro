FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 5000