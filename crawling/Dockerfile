FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip3 install -r requirements.txt
RUN python -m pip install --upgrade pip
RUN apt update && apt upgrade -y && apt install -y nginx

COPY nginx.conf.example /etc/nginx/nginx.conf
COPY nginx.sh /root/nginx.sh
RUN service nginx start

CMD ["python3","manage.py","runserver","0:7000"]
