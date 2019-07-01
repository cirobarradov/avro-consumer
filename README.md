# avro-consumer
Python process to print output kafka avro messages 

```console
docker run -ti -e BROKER_LIST=localhost:9092 -e SCHEMA_HOST=localhost -e SCHEMA_PORT=8081 -e TOPIC_LIST='topic1,topic2,topic3' cirobarradov/avro-consumer
```
