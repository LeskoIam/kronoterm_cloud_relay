python -m bumpver update --%1

docker build -t leskoiam/kronoterm_cloud_relay .
docker push leskoiam/kronoterm_cloud_relay