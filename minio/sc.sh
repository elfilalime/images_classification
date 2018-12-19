wget https://dl.minio.io/client/mc/release/linux-amd64/mc

chmod +x mc
./mc config host add minio http://0.0.0.0:9001 elfilali elfilali --api "s3v4" --lookup "auto"
./mc mb minio/datas
touch test.txt
./mc cp test.txt minio/datas
