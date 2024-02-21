FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY ./requirements.txt .
RUN pip install torch==2.2.0
RUN pip install -r requirements.txt
RUN pip install ultralytics
RUN pip install --ignore-installed opencv-python-headless
COPY ./app /app
COPY ./models /models
EXPOSE 8080
