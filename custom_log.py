import datetime
from fastapi.requests import Request

def log(tag="MyApp", message="no message", request: Request = None):
    with open("log.txt", "a") as log:  # Mode append to avoid overwriting
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{current_time} | {tag}: {message} | Endpoint: {request.url} | Method: {request.method}\n"
        log.write(log_entry)
