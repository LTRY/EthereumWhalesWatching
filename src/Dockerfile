FROM alpine:latest

RUN apk add --no-cache gcc && \
    echo "**** install python3-dev ****" && \
    apk add --no-cache python3-dev && \
    apk add libc-dev openssl-dev libffi-dev &&\
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    pip3 install cython requests web3 kafka-python aiohttp pymysql cryptography fire&& \
    pip3 install --pre gql[aiohttp]

WORKDIR /pi2
COPY ./utils.py /pi2
COPY ./producer.py /pi2
COPY ./consumer.py /pi2
CMD ["python"]
