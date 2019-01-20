FROM gettyimages/spark

ADD train.npy /home
ADD train_labels.npy /home
ADD split_data.py /home
ADD learning.py /home

RUN chmod 777 /home/split_data.py && \
     pip install elasticsearch && \
     pip install elephas && \
     pip install keras && \
     pip install pandas && \
     pip install minio && \
     pip install numpy
