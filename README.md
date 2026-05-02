# 🚀 Async Task Platform

Async Task Platform is a containerized backend system for processing background jobs using **FastAPI + Celery + Redis + PostgreSQL**, with integrated **Prometheus monitoring and Grafana dashboards**.

The project demonstrates a production-style architecture for asynchronous task execution with observability support.

---

# 🧠 Project Overview

The system allows users to:

* submit asynchronous tasks via REST API
* process tasks in background workers
* track task execution status
* store results in PostgreSQL
* monitor API performance using Prometheus
* visualize metrics in Grafana

This project simulates a simplified distributed job-processing backend similar to real-world task processing systems.

---

# 🏗️ Architecture

```
Client
   |
   v
FastAPI (API service)
   |
   v
PostgreSQL (task metadata storage)
   |
   v
Redis (message broker)
   |
   v
Celery Worker (background processing)
   |
   v
Prometheus → Grafana (monitoring)
```

---

# ⚙️ Tech Stack

Backend:

* FastAPI
* Celery
* Redis
* PostgreSQL
* SQLAlchemy

Monitoring:

* Prometheus
* Grafana

Infrastructure:

* Docker
* Docker Compose

---

# 🔄 Task Lifecycle

Task execution flow:

```
POST /task
   ↓
task stored in PostgreSQL
   ↓
Celery worker receives job via Redis
   ↓
worker updates status → STARTED
   ↓
task processed
   ↓
status updated → SUCCESS
   ↓
result stored in database
```

---

# 📦 Project Structure

```
async-task-platform
│
├── app
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── tasks.py
│
├── docker
│   └── Dockerfile
│
├── frontend
│   └── index.html
│
├── monitoring
│   └── prometheus.yml
│
├── docker-compose.yml
└── requirements.txt
```

---

# 🚀 Quick Start

## Run the project

Clone repository:

```
git clone https://github.com/karolkuzniak/async-task-platform.git
cd async-task-platform
```

Start services:

```
docker compose up --build
```

---

# 🌐 Available Services

| Service    | URL                   |
| ---------- | --------------------- |
| API        | http://localhost:8000 |
| Prometheus | http://localhost:9090 |
| Grafana    | http://localhost:3000 |

Grafana default credentials:

```
login: admin
password: admin
```

---

# 🔌 API Endpoints

## Create task

```
POST /task
```

Example:

```
{
  "data": "example task input"
}
```

Response:

```
{
  "task_id": "uuid"
}
```

---

## Get task status

```
GET /task/{task_id}
```

Response:

```
{
  "id": "...",
  "status": "SUCCESS",
  "result": "Processed: example task input"
}
```

---

## List all tasks

```
GET /tasks
```

---

## Metrics endpoint

```
GET /metrics
```

Used by Prometheus.

---

# 📊 Monitoring

Prometheus collects:

* request count
* request duration

Metrics exposed via:

```
/metrics
```

Grafana can be used to visualize:

* API latency
* request throughput
* system performance trends

---

# 🧪 Example Task Execution

Submit task:

```
curl -X POST http://localhost:8000/task \
-H "Content-Type: application/json" \
-d '{"data":"hello world"}'
```

Check result:

```
curl http://localhost:8000/task/{task_id}
```

---

# 🐳 Docker Services

The system runs as multiple containers:

```
api
worker
postgres
redis
prometheus
grafana
```

Worker processes tasks asynchronously using Celery.

---


Project demonstrates:

* async backend architecture
* message broker integration
* background task processing
* service orchestration with Docker Compose
* monitoring with Prometheus + Grafana
* production-style API structure


Author: https://github.com/karolkuzniak/
