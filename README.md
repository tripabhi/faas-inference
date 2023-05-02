# FaaS Inference

This is a project to demonstrate how ML Inference can be performed using Serverless Functions.

## Build and Deploy
```
./deploy.sh
```

http://10.52.0.189:5000/serve

# Example: curl -X POST -H "Content-Type: application/json" -d '{"data": "MESSAGE"}' http://GATEWAY_IP:PORT/serve
```
curl -X POST -H "Content-Type: application/json" -d '{"data": "MESSAGE"}' http://10.52.0.189:5000/serve

ab -n 100 -c 100 -e data.csv -p payload.json -T "application/json" http://10.52.0.189:5000/serve
```