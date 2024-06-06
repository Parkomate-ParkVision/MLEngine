<p align="center">
<img src="https://github.com/Parkomate-ParkVision/parkvision-frontend/assets/85283622/6f609ea7-b547-43cb-a771-2240ec86e914" width=400 />
</p>

# ParkVision MLEngine

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installation](#installation)

## Introduction

**ParkVision** is an advanced analytics dashboard designed for monitoring parking statistics and customer segmentation. This repository contains the MLEngine, a FastAPI-based application that handles the machine learning and AI components of ParkVision.

## Features

- **Machine Learning Models**: Implements models for predictive analytics and customer segmentation.
- **FastAPI**: High-performance API framework for serving ML models.
- **Real-time Predictions**: Provides real-time predictions and insights based on incoming data.
- **Scalability**: Designed to handle large volumes of data and requests efficiently.
- **Dockerized Deployment**: Simplified setup and deployment using Docker.

## Technologies

- **Python**: Main programming language for the MLEngine.
- **FastAPI**: Modern, fast (high-performance), web framework for building APIs with Python.
- **YOLO**: Object detection algorithms used for capturing vehicle information for parking analytics.
- **Docker**: Containerization platform for consistent environments.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Parkomate-ParkVision/MLEngine.git
cd MLEngine
```

**2. Build and Run the Docker Container with bash**

```bash
./run.sh start-dev
```

**3. Navigate to the following URL for the API documentation (Swagger/Redoc)**

```bash
http://localhost:8000/docs/
http://localhost:8000/redoc/
```

**4. Before pushing, run the check-syntax command and rectify the errors**

```bash
./run.sh check-syntax
```

**5. Stop the Docker Container with bash**

```bash
./run.sh stop-dev
```

<br>
<br>

![PARKVISION AHH ML](https://github.com/Parkomate-ParkVision/MLEngine/assets/67187699/5b18d7cb-e098-4cec-9c64-c86c1a9e9f68)
