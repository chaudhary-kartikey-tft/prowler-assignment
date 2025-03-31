# Prowler AWS Scanner with Django REST Framework (DRF)

This project provides a DRF application for running AWS security scans using [Prowler-CLI](https://docs.prowler.com/projects/prowler-open-source/en/latest/) and maintaining CRUD operations for scans, checks and findings. It also supports real-time status updates using Django Channels and WebSockets.

## Features
- Run **Prowler** AWS security scans in a **Celery** background task
- Store scan results (scans, checks, findings) in a PostgreSQL database
- Expost RESTful APIs for managing scan data using **Django Rest Framework (DRF)**
- Provide real-time scan status updates using **Django Channels & WebSockets**
- Run inside **Docker** with **Redis** for Celery task management

---

## Requirements
Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  
- AWS credentials configured (`~/.aws/credentials`)

---

## Setup & Installation

### Clone the repository
```sh
git clone https://github.com/chaudhary-kartikey-tft/prowler-assignment.git
cd prowler-assignment
```

### Create a `.env` file
Use the `.env.example` file in the project root and configure enviroment variables.
You would need to update the following environment variables:
- [SECRET_KEY](https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-SECRET_KEY) (use something like [Djecrety](https://djecrety.ir/) to generate a secret key)
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

### Build & Start Docker Containers
```sh
docker-compose up --build
```
This will start:  
- **Django API** (http://localhost:8000/)
- **PostgreSQL Database**  
- **Redis** (for Celery task queue)  
- **Celery Worker** (for running scans)
- **Nginx Server**
- **Django Channels WebSocket server** (ws://localhost:8000/)

