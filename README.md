## FastAPI Template Setup 

### 1. Clone the repository

```bash
git clone https://github.com/Parkomate-ParkVision/dashboard-ml.git
cd dashboard-ml
```

### 2. Install Docker and Docker Compose

[Install Docker](https://docs.docker.com/engine/install/)

[Install Docker Compose](https://docs.docker.com/compose/install/)

### 3. Build and Run the Docker Container with bash

```bash
./run.sh start-dev
```

### 4. Navigate to the following URL for the API documentation (Swagger/Redoc)

```bash
http://localhost:8000/docs/
http://localhost:8000/redoc/
```

### 5. Before pushing, run the check-syntax command and rectify the errors

```bash
./run.sh check-syntax
```
