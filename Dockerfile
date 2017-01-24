FROM alpine:3.5

RUN apk add --update \
    python \
    python-dev \
    py2-pip \
    build-base \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    py-cffi
RUN pip install Flask>=0.10.1
RUN pip install Jinja2>=2.8
RUN pip install MarkupSafe>=0.23
RUN pip install ncclient>=0.5.3
RUN pip install pyang>=1.7.1

COPY ./app /app
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

RUN rm -rf /var/cache/apk/*

EXPOSE 8000

CMD python app.py