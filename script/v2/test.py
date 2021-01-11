import pymysql
from kafka import KafkaProducer
from json import dumps
from sys import stdout
from time import sleep

msg = "Wait for it"

for i in range(6):
    stdout.write(f"\r{msg}, retrying in {5 - i} ")
    stdout.flush()
    sleep(1)