source .venv/bin/activate
python -m pip install -U -r prod_requirements.txt
nohup  uvicorn src.kronoterm_cloud_relay:app --host=0.0.0.0 --port=8555 &
