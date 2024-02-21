FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY ./app /app
COPY ./models /models
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install ultralytics
RUN pip install opencv-python-headless
RUN pip install -r requirements.txt
EXPOSE 8080
