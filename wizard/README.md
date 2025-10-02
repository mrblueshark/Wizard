# 🛡️ Wizard: Encrypted Data Pipeline

Wizard is a secure, end-to-end data pipeline designed to capture, encrypt, store, and analyze sensitive data with robust separation of concerns, ensuring data-at-rest is always protected by a dedicated Key Management Service (KMS).

## 💡 Why Wizard Exists

In many security and compliance-critical systems, data must be analyzed, but the raw, unencrypted data must never be stored directly in the main database. Wizard enforces the separation principle:

1.  **Collector** captures raw data.
2.  **Storage** service encrypts the data using a unique key per packet (managed by the KMS).
3.  **Analyzer** can only access the data after successfully retrieving the decryption key from the KMS.

This multi-service, multi-language approach (Go for high-speed collection, Python for secure storage/analysis) is typical in enterprise security environments.

## 📐 Architecture Overview

The system consists of four primary services communicating via gRPC (high-performance) and HTTP (for key management):

| Service | Language/Tool | Role | Communication |
| :--- | :--- | :--- | :--- |
| **collector** | Go (Client) | Captures simulated network packets and dispatches them to Storage via gRPC. | gRPC |
| **storage** | Python (Server) | Receives packets, encrypts payload using AES-GCM (via KMS), and saves the ciphertext to Postgres. | gRPC, HTTP (to KMS) |
| **kms-wrapper** | Python/FastAPI | Mock Key Management System. Stores Data Encryption Keys (DEKs) and Master Key IDs. | HTTP |
| **analyzer** | Python (Client) | Fetches encrypted packets from Postgres, decrypts them (via KMS), and runs simulated DSL queries using `pandas`. | HTTP (to KMS), Postgres |
| **postgres_db** | Postgres | Persistent storage for encrypted packets. | Postgres Protocol |

## 🛠️ Installation and Setup

### Prerequisites

You must have **Docker** and **Docker Compose** installed to run the entire pipeline locally.

### Usage

1.  **Build and Run the Services:**
    Navigate to the `wizard/deployments/` directory and run the following command to build all images and start the containers:

    ```bash
    docker compose up --build
    ```
    *(The services will start, and the Collector will begin dispatching packets every 2 seconds.)*

2.  **Monitor Output:**
    * The **`collector`** logs will show packets being sent (e.g., `Dispatching packet: <ID>`).
    * The **`storage`** logs will show packets being received, encrypted with a unique key, and saved (e.g., `DB WRITE: Saved encrypted data for ID: <ID>...`).
    * The **`analyzer`** logs will periodically retrieve data, decrypt it using the KMS, and run a simulated query (e.g., `Query Results: Found X matches.`).

3.  **Stop the Services:**
    Press `Ctrl+C` in the terminal, then run:

    ```bash
    docker compose down
    ```

## 🤝 Contribution Guide

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/new-telemetry`).
3.  Commit your changes following conventional commits (e.g., `feat: add prometheus metrics`).
4.  Open a Pull Request.
