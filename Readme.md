# Azure Document Portal

A containerized Flask application for uploading, listing, downloading, and deleting documents stored in **Azure Blob Storage**.

This project demonstrates Azure Storage integration, Docker containerization, secure application configuration, and Azure authentication using connection strings and Managed Identity.

## Features

- Upload documents to Azure Blob Storage
- List documents stored in a Blob container
- Download documents
- Delete documents
- 25 MB upload limit
- Secure filenames using Werkzeug
- Production application server using Gunicorn
- Dockerized application
- Support for Azure Managed Identity

## Architecture

### Current local development setup

```text
Browser
   |
   | HTTP :80
   v
Docker Container
   |
   | Flask + Gunicorn :8000
   |
   | Azure Storage SDK
   v
Azure Blob Storage
   |
   +-- documents container
```

Local Docker authentication uses an Azure Storage connection string supplied at runtime through an environment file.

### Planned Azure VM deployment

```text
Browser
   |
   v
Azure Linux VM
   |
   | Docker
   v
Flask + Gunicorn
   |
   | DefaultAzureCredential
   v
System-assigned Managed Identity
   |
   | Microsoft Entra ID token
   v
Azure Blob Storage
```

The Azure VM will use Managed Identity and Azure RBAC instead of a Storage Account connection string.

## Technologies

- Python 3
- Flask
- Gunicorn
- Azure Blob Storage
- Azure Identity SDK
- Azure Storage Blob SDK
- Docker
- Linux / Ubuntu
- Microsoft Entra ID and Azure RBAC

## Prerequisites

- Python 3.12 or later (for local Python development)
- Docker Desktop
- An Azure subscription
- An Azure Storage Account
- A Blob container named `documents`

## Configuration

The application uses environment variables.

| Variable | Description |
|---|---|
| `AZURE_STORAGE_ACCOUNT_NAME` | Azure Storage Account name |
| `AZURE_STORAGE_CONTAINER_NAME` | Blob container name |
| `AZURE_STORAGE_CONNECTION_STRING` | Optional connection string for local development |
| `FLASK_SECRET_KEY` | Flask session secret |
| `PORT` | Application port (default: 5000 for Flask development) |

Create a `.env` file in the project root:

```env
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account
AZURE_STORAGE_CONTAINER_NAME=documents
AZURE_STORAGE_CONNECTION_STRING=your-storage-connection-string
FLASK_SECRET_KEY=replace-with-a-random-secret
```

**Security:** Never commit `.env` or publish Storage Account keys. The `.env` file must be excluded through `.gitignore` and `.dockerignore`.

## Run with Docker

### 1. Build the image

```bash
docker build -t azure-document-portal:1.0 .
```

### 2. Start the container

```bash
docker run -d \
  --name document-portal \
  -p 80:8000 \
  --env-file .env \
  --restart unless-stopped \
  azure-document-portal:1.0
```

### 3. Open the application

Visit:

```text
http://localhost
```

### 4. View container logs

```bash
docker logs --tail 100 document-portal
```

### 5. Stop and remove the container

```bash
docker rm -f document-portal
```

## Authentication

The application supports two authentication approaches.

### Local development: Storage connection string

For local Docker development, the application can authenticate using a Storage Account connection string.

The connection string contains the Storage Account key and must be treated as a secret.

### Azure deployment: Managed Identity

When deployed to an Azure VM:

1. Enable the VM's system-assigned Managed Identity.
2. Assign the identity the `Storage Blob Data Contributor` role on the Storage Account or appropriate container scope.
3. Configure the Storage Account name and container name.
4. Do not provide `AZURE_STORAGE_CONNECTION_STRING`.
5. Allow `DefaultAzureCredential` to obtain a token using the VM's Managed Identity.

This removes the need to store Storage Account keys in the application configuration.

## Docker Image

The Docker image will be published to Docker Hub.

After publication, it can be pulled using:

```bash
docker pull DOCKERHUB_USERNAME/azure-document-portal:1.0
```

## Security Considerations

- Do not store credentials in the Dockerfile.
- Do not commit `.env` files.
- Use Managed Identity for Azure-hosted applications.
- Apply least-privilege RBAC permissions.
- Prefer private network connectivity to Storage where required.
- Use HTTPS for production application access.
- Keep the Docker image free of secrets.

## Project Status

| Component | Status |
|---|---|
| Flask application | Completed |
| Azure Blob Storage integration | Completed |
| Upload / List / Download / Delete | Tested successfully |
| Dockerfile and Gunicorn | Completed |
| Local Docker authentication | Tested successfully |
| GitHub publication | Pending |
| Docker Hub publication | Pending |
| Azure VM deployment with Managed Identity | Next stage |
| Private Endpoint and Private DNS integration | Planned |
| Azure Backup and restore demonstration | Planned |

## Learning Objectives

This project demonstrates practical experience with:

- Azure Blob Storage
- Azure SDK for Python
- Docker image creation and container execution
- Environment-based application configuration
- Azure authentication and authorization
- Microsoft Entra ID Managed Identity
- Azure RBAC
- Deploying containerized applications to Azure infrastructure
