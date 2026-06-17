# Face Service

Run:

uvicorn app:app --host 0.0.0.0 --port 8000 --reload

GET /health

POST /embedding
form-data key: file
