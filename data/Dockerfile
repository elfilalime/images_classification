FROM gettyimages/spark


ADD uploadfile.conf /etc/init.d
ADD uploadfile /etc/init.d
RUN chmod 777 /etc/init.d/uploadfile && \
     chmod 777 /etc/init.d/uploadfile.conf
