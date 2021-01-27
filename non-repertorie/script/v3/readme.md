
### What's changing:
- Remove binance query
- graphql from multiple blocks to one block

I. Go inside DockerFile directory
```shell script
~ cd docker
```
\
II. build img-python from Dockerfile
```shell script
~ docker build -t img-python .
```
\
III. build containers in the background
```shell script
~ docker-compose up --detach
```
Only building containers (+ on front)
```shell script
~ docker-compose up sql kafka-cluster
```
\
IV. View containers logs
```shell script
~ docker-compose logs --follow
```
\
V. Shutdown gracefully before backing up sql ETH databases  
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

Execute shutdown
```shell script
~ sh shutdown.sh
```
