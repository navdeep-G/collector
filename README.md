# **Collector**

A lightweight Tornado-based web application for managing file uploads, descriptions, and retrieval, backed by **MinIO** for file storage and **Redis** for metadata persistence.

---

## 🚀 **Overview**

**Collector** is a file management service built with **Tornado**, **MinIO**, and **Redis**. It provides endpoints for uploading files with descriptions, listing uploaded files, and downloading them securely. Designed for simplicity, scalability, and extensibility, it offers a streamlined way to handle file ingestion and retrieval workflows.

---

## 📚 **Key Features**

- 📂 **File Uploads:** Upload files with metadata descriptions using a web form.  
- 🗂️ **File Listings:** Browse uploaded files and their descriptions in a structured view.  
- ⬇️ **File Downloads:** Securely download files using UUID-based file names.  
- ⚡ **Asynchronous Processing:** Handles uploads and downloads efficiently with Tornado's async capabilities.  
- 🛡️ **Persistent Storage:** File storage via MinIO and metadata persistence via Redis.  
- 🧩 **Extensible Design:** Modular structure for easy enhancements and customization.  

## 📦 **1. Install Dependencies**

#### **1.1 Install Homebrew**

```bash
# If you don't have Homebrew installed:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ensure Homebrew is up-to-date:
brew update
```

#### **1.2 Install Redis**

```bash
brew install redis

# Start Redis as a service:
brew services start redis

# Verify Redis is running:
redis-cli ping

# You should see PONG if Redis is running correctly.

```

#### **1.3 Install Minio**

```bash
brew install minio/stable/minio

# Start MinIO with default configurations:
mkdir -p ~/minio/data
export MINIO_ROOT_USER=admin
export MINIO_ROOT_PASSWORD=password

minio server --console-address ":9001" ~/minio/data

# Console: Access MinIO's web interface at http://localhost:9001.
# Access Key: admin
# Secret Key: password
```

#### Update your .env file with the MinIO configuration:

```bash
MINIO_URL=http://localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=password
REDIS_URL=localhost
REDIS_PORT=6379
REDIS_DB=0
```

#### Verify both services:

```bash
Redis: redis-cli ping → PONG
MinIO: Access http://localhost:9001 and log in.
```

#### ** 1.4 Install Python Dependencies**

```bash
git clone https://github.com/navdeep-G/collector.git
cd collector

pip install -r requirements.txt

python example/app.py

```

## ⚡ **Quickstart Guide**

### Access the Web UI:

- **Upload Files:** Visit [http://localhost:8888/add](http://localhost:8888/add) to upload a file with a description.  
- **View Files:** Visit [http://localhost:8888/](http://localhost:8888/) to see a list of uploaded files.  
- **Download Files:** Access files via `http://localhost:8888/file/<file_uuid>`.

---

### API Endpoints:

| **Method** | **Route**            | **Description**        |
|------------|-----------------------|-------------------------|
| GET        | `/`                  | List uploaded files     |
| GET        | `/add`               | File upload form        |
| POST       | `/add`               | Upload file             |
| GET        | `/file/<file_uuid>`  | Download specific file  |

### Example CURL Upload:

```bash
curl -F "description=Sample File" -F "file=@path/to/file.txt" http://localhost:8888/add
```

## **Project Structure**

```bash
collector/
├── controllers.py   # Tornado request handlers for API endpoints
├── models.py        # Logic for file handling, validation, and storage
├── routes.py        # URL route definitions
├── example/         # Example usage scripts and templates
│   ├── templates/   # HTML templates for UI
│   ├── static/      # Static assets (CSS/JS)
│   ├── app.py       # Example Tornado application
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```
