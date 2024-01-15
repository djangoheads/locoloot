bind = "0.0.0.0:8000"
workers = 3
worker_class = "service.uvicorn.TruelyWorker"
max_requests = 100
max_requests_jitter = 2
preload_app = True
