# 🧙 Wizard: Cross-Language Data Processing Platform

## 🌟 Project Overview
The **Wizard** project is a high-performance, distributed application designed for real-time data ingestion, analysis, and processing. It employs a microservices architecture utilizing the best-fit language for each task:

1.  **Go Collector Service**: Handles high-throughput data collection, validation, and standardization.
2.  **Python Analyzer/API Service**: Provides the public-facing API and executes complex data analysis, machine learning inference, and business logic.

## 🚀 Getting Started (Local Development)

To spin up the entire application stack (Go, Python, PostgreSQL, and Kafka) locally, you only need **Docker** and **Docker Compose**.

1.  **Environment Setup:** Ensure the local environment variables are sourced (these are automatically picked up by Docker Compose):
    ```bash
    source default.env
    ```

2.  **Build and Run:** Use Docker Compose to build the custom images and start all dependent services:
    ```bash
    docker-compose up --build
    ```

### Local Endpoints:
* **Python API (Analyzer):** `http://localhost:9000`
* **Go Collector (Health Check):** `http://localhost:8080`

## 🛠️ Architecture and Stack

| Component | Language/Technology | Purpose | Location |
| :--- | :--- | :--- | :--- |
| **Collector** | Go | High-throughput ingestion, event standardization. | `go/collector` |
| **Analyzer/API** | Python (FastAPI) | Business logic, complex data analysis, public API. | `python/wizard` |
| **Database** | PostgreSQL | Persisting analysis results and system state. | Managed via Docker/K8s |
| **Messaging** | Kafka | Asynchronous event streaming between services. | Managed via Docker/K8s |
| **Deployment** | Kubernetes, GitHub Actions | Production and CI/CD orchestration. | `.github`, `deployments/k8s` |

## 🧪 Testing

### Go Tests
Navigate to the `go/` directory and run:
```bash
go test ./...
```

### Python Tests
Navigate to the `python/` directory and run:
```bash
pytest
```

---

## ☁️ Deployment

Production deployment is managed via **GitHub Actions** () targeting a Kubernetes cluster, utilizing Helm charts (WIP) and the manifest files found in `deployments/k8s/`.

