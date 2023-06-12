# FaaS Inference

This is a project to demonstrate how ML Inference can be performed using Serverless Functions.

## Build and Deploy
```
./deploy.sh
```

http://10.52.0.189:5000/serve

# Example: curl -X POST -H "Content-Type: application/json" -d '{"data": "MESSAGE"}' http://GATEWAY_IP:PORT/serve
```
curl -X POST -H "Content-Type: application/json" -d '{"data": "MESSAGE"}' http://127.0.0.1:7000/infer
curl -X POST -H "Content-Type: application/json" -d '{"data": "MESSAGE"}' http://10.52.0.201:7000/infer

ab -n 100 -c 100 -e data.csv -p /home/cc/anish/faas-inference/loadgen/payload.json -T "application/json" http://10.52.0.201:7000/infer
```
sudo ln -s /home/cc/anish/faas-inference/loadgen/script.sh /usr/bin/loadscript