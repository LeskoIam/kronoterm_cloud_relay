cd src || exit
python -m flask --app kronoterm_cloud_relay --debug run --host=0.0.0.0 --port=8555