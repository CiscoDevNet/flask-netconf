#
# Take a minimal base
#
FROM alpine:3.5

#
# Batch commands to optimize container size. The build-tools and -dev
# versions of various libs are needed to build some of the Python
# modules, hence why the pip install phase is embedded between package
# adds and dels. Splitting this up into multiple RUN statements will
# bloat container to approx 268MB at time of writing, compared to 97MB
# with this approach.
#
RUN apk add --update \
    python \
    python-dev \
    py2-pip \
    libxml2 \
    libxml2-dev \
    libxslt \
    libxslt-dev \
    openssl \
    openssl-dev \
    py-cffi \
    build-base \
    && \
    pip install \
        Flask>=0.10.1 \
        Jinja2>=2.8 \
        MarkupSafe>=0.23 \
        ncclient>=0.5.3 \
        pyang>=1.7.1 \
    && \
    apk del --update \
        build-base \
	openssl-dev \
	libxslt-dev \
	libxml2-dev \
    && \
    rm -rf /var/cache/apk/* \
    && \
    mkdir -p ~/.ssh \
    && \
    printf "StrictHostKeyChecking no\nHostKeyAlgorithms +ssh-dss\nKexAlgorithms +diffie-hellman-group1-sha1\n" \\
        >> ~/.ssh/config \
    && \
    chmod -R 600 ~/.ssh


COPY ./app /app

WORKDIR /app

EXPOSE 8000

CMD python app.py
