# Python Microservices Demo

> learn from: https://www.bilibili.com/video/BV1SG4y1G7uN?p=1  thanks

## OS

Windows11

## Language && Files format

Python3.10.x
Yaml (for k8s)
Dockerfile (build image)
txt (python flask requirements.txt)

## IDE && Tools

Docker Desktop (required)
Pycharm (optional, coding)

## Docker Images

- MySQL (mine is 8.0.x)
- Mongo (latest)

## Prepare

- Download kubectl from https://kubernetes.io/docs/tasks/tools/   (for me, I use binary package to install)
- Register an account from https://hub.docker.com/, we will use it to push our build images
- Download minikube from https://minikube.sigs.k8s.io/docs/start/ to install
- Install k9s command window from https://github.com/derailed/k9s
- Start docker desktop, start MySQL and Mongo images

## for auth services
```bash
D:\pycharm\workspace\system_design\venv\Scripts\python.exe -m pip install --upgrade pip
pip install pyjwt
pip install flask_mysqldb
pip install flask
pip3 freeze > requirements.txt
docker build .
docker tag 461161b3c7e3daf928f94fa025e04884fa75c72d1a0669da5cf98edcc5dce1ae chumingcheng/auth:latest
docker images
docker push chumingcheng/auth:latest
docker pull chumingcheng/auth:latest
kubectl apply -f ./
k9s
```


## edit hosts
```bash
# hosts file add
127.0.0.1 mp3converter.com
127.0.0.1 rabbitmq-manager.com
```


## for rabbitmq service
```bash
kubectl apply -f ./
k9s
kubectl describe pod rabbitmq-0
kubectl describe pvc
kubectl delete -f ./
kubectl apply -f ./
rabbitmq-manager.com
minikube tunnel
# close vpn and access rabbitmq-manager.com in browser (vpn will cause trouble)
```



## for gateway service
```bash
pip install pika
pip freeze > requirements.txt
docker build .
docker tag dc0763aca5dc102994eb25cad2796ba017939ad4ee5759c5443877cf1f6e552d chumingcheng/gateway:latest
docker push chumingcheng/gateway:latest 
minikube addons list
#edit k8s yaml
minikube addons enable ingress
minikube tunnel
kubectl apply -f ./
k9s
kubectl scale deployment --replicas=0 gateway
```




## for converter service
```bash
python3 -m venv venv
source ./venv/bin/activate
env | grep ENV
cat consumer.py |head -n 10
pip install pika, pymongo
pip install moviepy
pip install jedi pylint
pip freeze > requirements.txt
docker build .
docker tag b590d490e3de34f4c080af6f07ee40655cdc1c2f4d34af352c0282fd2d2ee36a chumingcheng/converter:latest
docker push chumingcheng/converter:latest
kubectl apply -f ./
kubectl logs -f converter-66f9d75b49-4cbcb
```



## test upload service
```bash
curl -X POST http://mp3converter.com/login -u georgio@email.com:Admin123

kubectl get pods
error: 
  TypeError: 'str' object cannot be interpreted as an integer
  cur = mysql.connection.cursor()

curl -X POST http://127.0.0.1:5000/login -u georgio@email.com:Admin123
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


C:\Users\Lenovo>curl -X POST http://mp3converter.com/login -u georgio@email.com:Admin123
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlb3JnaW9AZW1haWwuY29tIiwiZXhwIjoxNjgyMjQ0MjY5LCJpYXQiOjE2ODIxNTc4NjksImFkbWluIjp0cnVlfQ.QFBDMEIQa9YzizNcUBRMoDBzvqmm5Xxa1kr0qv0F5qU


curl -X POST -F 'file=@./test.mp4' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlb3JnaW9AZW1haWwuY29tIiwiZXhwIjoxNjgyMjQ0MjY5LCJpYXQiOjE2ODIxNTc4NjksImFkbWluIjp0cnVlfQ.QFBDMEIQa9YzizNcUBRMoDBzvqmm5Xxa1kr0qv0F5qU' http://mp3converter.com/upload

Invoke-WebRequest : 无法绑定参数“Headers”。无法将“System.String”类型的“Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlb3JnaW9AZW1haWwuY29tIiwiZXh      
wIjoxNjgyMjQ0MjY5LCJpYXQiOjE2ODIxNTc4NjksImFkbWluIjp0cnVlfQ.QFBDMEIQa9YzizNcUBRMoDBzvqmm5Xxa1kr0qv0F5qU”值转换为“System.Collections.IDictionary”类型。
所在位置 行:1 字符: 39
+ ... est.mp4' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgument: (:) [Invoke-WebRequest]，ParameterBindingException
    + FullyQualifiedErrorId : CannotConvertArgumentNoMessage,Microsoft.PowerShell.Commands.InvokeWebRequestCommand


kubectl scale deployment --replicas=1 gateway
kubectl scale deployment --replicas=1 converter auth
kubectl get pods
kubectl logs -f gateway-bb8b5b499-9w67p
kubectl get pods
kubectl logs -f gateway-bb8b5b499-9w67p
kubectl get pods
kubectl logs -f converter-66f9d75b49-d6pfr


windows powershell
Get-Help Invoke-WebRequest


add some logs:
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(lineno)d:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


docker pull mongo  && start


2023-04-22 11:44:22,246 util.py:33:INFO:Traceback (most recent call last):
  File "/app/storage/util.py", line 23, in upload
    channel.basic_publish(
  File "/usr/local/lib/python3.10/site-packages/pika/adapters/blocking_connection.py", line 2259, in basic_publish
    self._impl.basic_publish(
  File "/usr/local/lib/python3.10/site-packages/pika/channel.py", line 423, in basic_publish
    self._raise_if_not_open()
  File "/usr/local/lib/python3.10/site-packages/pika/channel.py", line 1403, in _raise_if_not_open
    raise exceptions.ChannelWrongStateError('Channel is closed.')
pika.exceptions.ChannelWrongStateError: Channel is closed.

gateway: connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", heartbeat=0))
```



## test success then check mongo
```bash
# connect local mongodb from pycharm
show databases
use mp3s
show collections
db.fs.files.find()
db.fs.files.find({"_id":ObjectId("6443d2ca6e6dbcbca60dc3b4")})
# below command can export mp3 files from mongodb, according to GridFS
# I use docker desktop in windows, I didn't find the mongofiles.exe executable file outside docker, I should mount the volume first but I forgot, so I didn't test it from windows
mongofiles --db=mp3s get_id --local=test.mp3 '{"$oid":"6443d2ca6e6dbcbca60dc3b4"}'
# I just test it from docker internal
./mongofiles  --db=mp3s get_id --local=test.mp3 '{"$oid":"6443d2ca6e6dbcbca60dc3b4"}'
```


## for gateway download interface
```bash
# write download interface code and then execute below commands
docker build .
docker tag 46a12c0dae73bc34cf5bd54c63f29feaaf68324a927bd6c0ea03a5dc44337818 chumingcheng/gateway:latest
docker push chumingcheng/gateway:latest
kubectl delete -f .\manifests\
kubectl apply -f .\manifests\
```

## for notification service

- copy Dockerfile from gateway and do some small modifications
- copy manifests from converter and do some small modifications


## usage shortcut

![img.png](img.png)

![img_1.png](img_1.png)

![img_3.png](img_3.png)

![img_2.png](img_2.png)