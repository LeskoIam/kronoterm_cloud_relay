source .venv/bin/activate
cd src || exit
nohup flask --app kronoterm_cloud_relay run --host=0.0.0.0 --port=8555 &