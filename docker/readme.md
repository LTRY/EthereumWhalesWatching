#0. Get Geth running
```shell script
~ geth --syncmode full --nousb --cache 1024 --datadir=/Volumes/ETH/.ethereum/.ethereum \
    --ipcpath=~/IPC/geth.ipc --http --http.api eth,web3,personal --graphql --maxpeers 0
```

## Standart use
\
I. Go inside DockerFile directory
```shell script
~ cd docker
```
\
II. Build img-python from Dockerfile
```shell script
~ docker build -t img-python .
```
\
III. Build containers in the background
```shell script
~ docker-compose up --detach
```
\
IV. View containers logs
```shell script
~ docker-compose logs --follow
```
\
V. Shutdown gracefully before backing up sql ETH databases  
```shell script
~ sh shutdown.sh
```
`shutdown.sh`:
```shell script
if [ "$(docker ps -q -f name=sql)" ]; then
    echo "...Move the last backup to a safe place if this goes wrong..."
    mv /Volumes/ETH/pi2/sql/mysql-dump/backupiswhale.sql /Volumes/ETH/pi2/sql/backup || $1
    
    echo '...Regsiter the new backup. Dumping iswhale table...'
    docker exec -i sql mysqldump -ppwd ETH iswhale > /Volumes/ETH/pi2/sql/mysql-dump/backupiswhale.sql 
fi

echo '...docker-compose kill...'
docker-compose kill
```

## Run py-producer & py-consumer in local | kafka-cluster & sql in docker
\
I. Go inside DockerFile directory
```shell script
~ cd docker
```
\
II. Build img-python from Dockerfile
```shell script
~ docker build -t img-python .
```
\
III. Docker-compose sql & kafka-cluster containers
```shell script
~ docker-compose up sql kafka-cluster
```
\
IV. Open 2 other shells and enter the virtual env
```shell script
~ cd docker
~ source ../../venv/bin/activate
```
\
V. Run py-consumer & py-producer
```shell script
~ python producer.py --local=True --fromFlagBlock=11000000
~ python consumer.py --local True --logs True --waitGethSync False --txTriggeringValue 100000
```

## Run py-producer & py-consumer in local | kafka-cluster in docker | sql excluded
\
I. Go inside DockerFile directory
```shell script
~ cd docker
```
\
II. Build img-python from Dockerfile
```shell script
~ docker build -t img-python .
```
\
III. Docker-compose sql & kafka-cluster containers
```shell script
~ docker-compose up kafka-cluster
```
\
IV. Create a virtual env
```shell script
~ virtualenv create
~ pip install -r requirements
```
\
V. Open 2 other shells and enter the virtual env
```shell script
~ cd docker
~ source venv/bin/activate
```
\
VI. Run py-consumer & py-producer
```shell script
~ python producer.py --local=True --fromFlagBlock=11000000
~ python consumer.py --local True --logs True --waitGethSync False --txTriggeringValue 100000 \
    --analyseTX False --recordSuspectTx False --sql False
```