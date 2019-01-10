FROM gettyimages/spark


ADD uploadfile /home

ADD split_data.py /home

RUN cd /home && \
     apt-get update && \
     apt-get install wget && \
     wget https://dl.minio.io/client/mc/release/linux-amd64/mc && \
     chmod +x mc

RUN chmod 777 /home/uploadfile && chmod 777 /home/split_data.py
