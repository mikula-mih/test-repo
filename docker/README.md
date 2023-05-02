
```bash
pip install -r requirements.txt
# run the code locally (without Docker):
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
# build and run the Docker image locally, as follows:
docker build -t channel-api .
docker run -d -p 8080:80 channel-api
# run example server with docker compose
docker-compose up --build
```

