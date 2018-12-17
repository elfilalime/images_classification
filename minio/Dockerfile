FROM golang:1.10.1-alpine3.7

LABEL maintainer="Minio Inc <dev@minio.io>"

ENV GOPATH /go
ENV PATH $PATH:$GOPATH/bin
ENV CGO_ENABLED 0
ENV MINIO_UPDATE off
ENV MINIO_ACCESS_KEY_FILE=access_key \
    MINIO_SECRET_KEY_FILE=secret_key

WORKDIR /go/src/github.com/minio/

RUN apk add --no-cache git && \
     git clone https://github.com/minio/minio /tmp/minio && \
     cp /tmp/minio/dockerscripts/docker-entrypoint.sh /tmp/minio/dockerscripts/healthcheck.sh /usr/bin/ && \
     rm -rf /tmp/minio

RUN  \
     apk add --no-cache ca-certificates 'curl>7.61.0' && \
     apk add --no-cache --virtual .build-deps git && \
     echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf && \
     go get -v -d github.com/minio/minio && \
     cd /go/src/github.com/minio/minio && \
     go install -v -ldflags "$(go run buildscripts/gen-ldflags.go)" && \
     rm -rf /go/pkg /go/src /usr/local/go && apk del .build-deps

RUN go get -d github.com/minio/mc && \
     cd ${GOPATH}/src/github.com/minio/mc && \
     make

WORKDIR /~

RUN mc mb minio-dcos/mh9-test && \
     touch test.txt && mc cp test.txt minio-dcos/mh9-test

EXPOSE 9001

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]

VOLUME ["/data"]

HEALTHCHECK --interval=30s --timeout=5s \
    CMD /usr/bin/healthcheck.sh

CMD ["minio"]
