# Kubernetes Deployment, Scaling & Rolling Update Notes

## 1. Cluster Setup & Image Ingestion
* **Cluster Startup**: Started local Minikube cluster via `minikube start`.
* **Image Loading**: Loaded container images into Minikube without an external registry using:
  ```bash
  minikube image load backend:latest
  minikube image load frontend:latest