source .venv/bin/activate
python -m pip install -U -r prod_requirements.txt
nohup fastapi run src/kronoterm_cloud_relay.py --host=0.0.0.0 --port=8555 &
