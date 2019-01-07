FROM golang:1.10.1-alpine3.7

WORKDIR /go

RUN wget https://dl.minio.io/client/mc/release/linux-amd64/mc

RUN chmod +x mc && \
     ./mc config host add minio http://0.0.0.0:9001 elfilali elfilali --api "s3v4" --lookup "auto" && \
     ./mc mb minio/datas && \
     ./mc cp test.txt minio/datas
