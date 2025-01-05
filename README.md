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
