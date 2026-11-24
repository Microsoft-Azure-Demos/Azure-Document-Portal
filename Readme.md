# Azure Document Portal

A lightweight Flask web application for uploading, listing, downloading, and deleting documents stored in **Azure Blob Storage**.

This application serves as the workload for my Azure Storage and Data Protection project, where I demonstrate secure cloud storage, private connectivity, identity-based access, storage lifecycle management, and disaster recovery using Terraform.

## Overview

The Document Portal provides a simple web interface for managing files stored in Azure Blob Storage. Instead of storing documents locally on the web server, the application uses Azure Blob Storage as its centralized storage backend.

The application is designed to evolve from local development using Azure CLI authentication to deployment on an Azure Virtual Machine using Managed Identity.

## Features

- **Upload:** Upload files to Azure Blob Storage.
- **List:** Display documents stored in a Blob container.
- **Download:** Retrieve and download stored documents.
- **Delete:** Remove documents from Blob Storage.
- **Azure Authentication:** Uses `DefaultAzureCredential` to support local Azure CLI authentication and Azure Managed Identity.
- **Upload Restrictions:** Enforces a maximum upload size of 25 MB.

## Architecture

```text
┌────────────────────┐
│    Web Browser    │
└─────────┬──────────┘
          │ HTTP
          ▼
┌────────────────────┐
│   Flask Web App    │
│                    │
│ Upload / List      │
│ Download / Delete  │
└─────────┬──────────┘
          │ Azure SDK
          │ Authentication
          ▼
┌────────────────────┐
│ Azure Blob Storage │
│                    │
│ Container:documents│
└────────────────────┘
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework |
| Azure Blob Storage | Cloud document storage |
| Azure Storage Blob SDK | Blob storage operations |
| Azure Identity SDK | Azure authentication |
| HTML / CSS | User interface |
| Azure CLI | Local development authentication |

## Project Structure

```text
azure-document-portal/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## Prerequisites

- Python 3.10+
- Azure CLI
- An Azure Storage Account
- A Blob container named `documents`
- Azure account with appropriate Blob data permissions

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/azure-document-portal.git
cd azure-document-portal
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Authenticate with Azure

For local development, authenticate using Azure CLI:

```bash
az login
```

Verify your active subscription:

```bash
az account show
```

The authenticated identity must have an appropriate Blob data role, such as **Storage Blob Data Contributor**, assigned at the relevant scope.

### 5. Configure environment variables

Set the Storage Account name and Blob container.

**Windows PowerShell:**

```powershell
$env:AZURE_STORAGE_ACCOUNT_NAME = "your_storage_account_name"
$env:AZURE_STORAGE_CONTAINER_NAME = "documents"
$env:FLASK_SECRET_KEY = "your_secret_key"
$env:PORT = "5000"
```

**Linux/macOS:**

```bash
export AZURE_STORAGE_ACCOUNT_NAME="your_storage_account_name"
export AZURE_STORAGE_CONTAINER_NAME="documents"
export FLASK_SECRET_KEY="your_secret_key"
export PORT="5000"
```

Replace the placeholder values with your own configuration.

### 6. Run the application

```bash
python app.py
```

Open the application in your browser:

[http://localhost:5000](http://localhost:5000)

## Azure Storage Configuration

The application connects to Azure Blob Storage using the Storage Account endpoint:

```text
https://<storage-account-name>.blob.core.windows.net
```

The target Blob container is configured through an environment variable.

### Authentication

The application uses `DefaultAzureCredential` from the Azure Identity SDK.

This supports different authentication methods depending on the environment:

| Environment | Authentication |
|---|---|
| Local development | Azure CLI credentials |
| Azure VM | Managed Identity |
| Other supported Azure environments | Environment-appropriate credentials |

Storage access is authorized through Azure RBAC data roles rather than embedding Storage Account keys in the application.

## Application Screenshots

Screenshots of the Document Portal can be added here to demonstrate the interface and functionality.

```text
screenshots/
├── portal.png
├── upload.png
└── documents-list.png
```

## Security Considerations

This application is designed to support a secure Azure deployment:

- Storage Account public network access can be disabled.
- Private Endpoint can be used for private Storage connectivity.
- Private DNS enables internal resolution of the Storage endpoint.
- Managed Identity eliminates the need to store Azure credentials in the application.
- Azure RBAC controls access to Blob Storage data.
- Uploaded files are restricted to a maximum size of 25 MB.

Additional application-level security, such as user authentication, file type validation, malware scanning, and production-grade deployment configuration, would be required before exposing the application to real users.

## Related Infrastructure Project

This application is part of my Azure Infrastructure as Code portfolio.

**Project 03 — Azure Storage and Data Protection**

The infrastructure project uses Terraform to provision and configure:

- Azure Storage Account
- Blob Containers
- Storage Lifecycle Management
- Private Endpoint
- Private DNS Zone
- Managed Identity
- Azure RBAC
- Recovery Services Vault
- Azure VM Backup
- Backup and recovery testing

The infrastructure repository will demonstrate deploying this application on an Azure VM and accessing Blob Storage through private networking.

## Learning Objectives

- Integrating a Python application with Azure Blob Storage.
- Implementing file upload, download, listing, and deletion.
- Using Azure SDKs to interact with cloud services.
- Understanding Azure authentication with `DefaultAzureCredential`.
- Preparing applications for Managed Identity.
- Separating application workloads from infrastructure provisioning.
- Supporting secure cloud application architectures.

## License

This project is intended for learning, experimentation, and portfolio demonstration purposes.
