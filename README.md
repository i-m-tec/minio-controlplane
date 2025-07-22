# Minio in ControlPlane Demo
[minio](https://min.io/) is an S3 compatible storage solution.  
[ControlPlane](https://controlplane.com) is a multi-cloud platform.
This demo deploys a workload that runs minio in a single ControlPlane GVC.
## YouTube Demo
[![MinIO in ControlPlane.com Demo](https://img.youtube.com/vi/H3ghTttSLuM/0.jpg)](https://www.youtube.com/watch?v=H3ghTttSLuM)

# Prep
## ControlPlane CLI
Install or updated `cpln`
```sh
npm install -g @controlplane/cli
```
Follow the documentation to configure `cpln`: https://docs.controlplane.com/quickstart/quick-start-3-cli
## MinIO Client
```sh
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/
```
# Deploy
```sh
cpln apply -f minio-demo.yaml --gvc demo
```
## Nginx Configuration
## Log into the nginx container
Use the web shell or copy the connect command using `sh` shell for the `nginx:alpine` container:
```sh
cpln workload connect minio --location aws-us-east-2 --container nginx --shell sh --org inertia-labs-inc-46f665 --gvc demo
```
## Console root
Replace nginx.conf and restart nginx.
```sh
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
vi /etc/nginx/nginx.conf
nginx -t
nginx -s reload
```
## API root
Change the port to `9000` on the `proxy_pass` line and restart nginx.

# Test API
## minio client
Test using minio client `mc`:
```sh
echo "This is a demo test" > test.txt
mc alias ls
mc alias set demo https://minio.demo.inertialabs.io minioadmin minioadmin
mc mb demo/mybucket
mc cp test.txt demo/mybucket
mc ls demo
mc ls demo/mybucket
mc cp demo/mybucket/test.txt ./downloaded.txt
cat downloaded.txt
mc rm demo/mybucket/test.txt
mc ls demo/mybucket
```
## python S3
Pass the workload url to minio-test.py:
```
python3 miniotest.py https://minio.demo.inertialabs.io
```
