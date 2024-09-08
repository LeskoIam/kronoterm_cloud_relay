source .venv/bin/activate
python -m pip install -U -r prod_requirements.txt
cd src || exit
nohup flask --app kronoterm_cloud_relay run --host=0.0.0.0 --port=8555 &