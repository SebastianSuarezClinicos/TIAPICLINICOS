gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 main:app
pip install -r requirements.txt