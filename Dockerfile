#
# Take a minimal base
#
FROM alpine:3.8

#
# Batch commands to optimize container size. The build-tools and -dev
# versions of various libs are needed to build some of the Python
# modules, hence why the pip install phase is embedded between package
# adds and dels. Splitting this up into multiple RUN statements will
# bloat container to approx 268MB at time of writing, compared to 97MB
# with this approach.
#
RUN apk add --update --no-cache \
        redis \
        python3 \
	py3-cffi \
        py3-paramiko \
        py3-flask \
        py3-jinja2 \
        py3-markupsafe \
        py3-lxml && \
    python3 -m ensurepip && \
    pip3 install -U pip && \
    pip3 --verbose install \
        pyang>=1.7.8 \
        ncclient>=0.6.3

COPY ./app /app
COPY boot.sh /boot.sh

WORKDIR /app

EXPOSE 8000

# CMD python3 app.py
# CMD ["/sbin/init"]
CMD ["/boot.sh"]