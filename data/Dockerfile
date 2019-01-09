FROM gettyimages/spark


ADD uploadfile /home

RUN cd /home && \
     apt-get update && \
     apt-get install wget && \
     wget https://dl.minio.io/client/mc/release/linux-amd64/mc && \
     chmod +x mc

RUN chmod 777 /home/uploadfile
