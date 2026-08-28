# Docker Containerization & Health Check Verification Log

## 1. Architecture Overview
* **Multi-Stage Dockerfile**: Uses a slim python 3.11 base image with a builder stage to isolate build dependencies and minimize final image footprint.
* **Health Probe**: Incorporates an explicit `HEALTHCHECK` instruction querying `http://localhost:8000/health`.
* **Docker Compose**: Orchestrates `backend` (FastAPI) and `frontend` (Streamlit) services, mounting persistent volumes for vector storage and loading credentials securely via `env_file`.

---

## 2. Local Build & Health Verification Log

* **Build & Start Command**:
  ```bash
  docker compose up --build