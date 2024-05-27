FROM python:3.10.8-slim-bullseye
USER root

# Language settings
RUN apt-get update && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt-get install -y vim less

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# Python settings
WORKDIR /app

COPY ./docker/python/requirements.txt ./
RUN pip install -r requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY ./ ./

# ポートの公開
EXPOSE 5000

# 環境変数の設定
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Flaskアプリケーションを実行
CMD ["flask", "run"]