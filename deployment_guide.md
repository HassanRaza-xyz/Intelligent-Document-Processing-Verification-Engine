# Deployment Guide: Intelligent Document Processing Engine

## Docker Deployment
This application is fully containerized and includes system-level dependencies for OpenCV and Tesseract OCR.

### Prerequisites
* Docker installed on your host machine.

### Build and Run Instructions

**1. Build the Docker Image**
Run this command in the root directory where the `Dockerfile` is located:
\`\`\`bash
docker build -t ezitech-document-engine .
\`\`\`

**2. Run the Container**
Start the container and map it to port 8000:
\`\`\`bash
docker run -d -p 8000:8000 --name doc-engine ezitech-document-engine
\`\`\`

**3. Access the Application**
* API Swagger UI: `http://localhost:8000/docs`
* API Root: `http://localhost:8000/`

**Note on Database:**
By default, this Docker setup uses SQLite. For a production environment, you should mount a Docker volume for the SQLite database or update `SQLALCHEMY_DATABASE_URL` in `app/database.py` to point to a managed PostgreSQL instance.