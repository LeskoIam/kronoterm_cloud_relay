docker image ls

docker build -t leskoiam/kronoterm_cloud_relay:0.0.8 .
docker image ls

docker tag leskoiam/kronoterm_cloud_relay:0.0.8 leskoiam/kronoterm_cloud_relay:latest
docker image ls

docker push leskoiam/kronoterm_cloud_relay:0.0.8
docker push leskoiam/kronoterm_cloud_relay:latest