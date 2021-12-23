FROM alpine:3.12
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/proyecto/
COPY . /home/proyecto/
WORKDIR /home/proyecto/

RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font
RUN apk add gcc musl-dev python3-dev pango zlib-dev jpeg-dev openjpeg-dev g++ libffi-dev
RUN apk add python3 python3-dev
RUN apk add py3-pip
RUN apk add py3-psycopg2
RUN apk add zip
RUN apk add redis


RUN pip3 install --upgrade pip
RUN pip3 install -r /home/proyecto/requirements.txt
RUN python3 /home/proyecto/files/html_1_13/setup.py install
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py loaddata /home/proyecto/files/backup_SUR_base.json
