FROM gettyimages/spark

RUN cd ~ && \
     apt-get update && \
     apt-get install wget && \
     wget https://dl.minio.io/client/mc/release/linux-amd64/mc

RUN cd ~ && \
     chmod +x mc && \
     ./mc config host add minio http://minio:9000 elfilali elfilali --api "s3v4" --lookup "auto" && \
     ./mc mb minio/datas && \
     touch test.txt && \
     ./mc cp test.txt minio/datas
