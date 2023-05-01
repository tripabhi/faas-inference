sudo docker build --tag faas-inference .
sudo docker run -d -v $(pwd)/data:/faas-inference/data -p 5000:5000 faas-inference