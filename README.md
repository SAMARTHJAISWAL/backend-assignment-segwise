# Event Trigger Platform

## Overview
The **Event Trigger Platform** is an application where users can manage event triggers that get activated based on certain conditions. It supports two types of triggers:

1. **Scheduled Triggers**:  
   - Fire at a fixed time or interval.  
   - Can be one-time or recurring .  

2. **API Triggers**:  
   - Triggered by sending an API request with predefined schema and values.  

Users can also test the triggers without saving them permanently. The platform provides a comprehensive event log system that archives and deletes event logs after a specific period.

---

## Features

- Create, edit, and delete triggers.
- View active and archived event logs.
- Test triggers manually (both API and scheduled).
- Event logs retention:
  - Active for 2 hours.
  - Archived for an additional 46 hours before deletion.
- UI for trigger management and event logs.

---

## Deployment

### Deployed Application
- **Frontend (Vercel):** [https://backend-assignment-segwise.vercel.app/]
- **Backend (Render):** [https://backend-assignment-segwise.onrender.com/]

---

## API Endpoints

### 1. Create Trigger
**Endpoint:** `POST /triggers/`  
**Payload:**  
```json
{
  "name": "Test Trigger",
  "type": "scheduled",
  "payload": "Sample Payload",
  "schedule_time": "2025-01-26T15:00:00"
}
```

### 2. View Triggers
**Endpoint:** `GET /triggers/`  
**Headers:**  
```json
{
  "X-API-KEY": "your-secure-secret-key-123456"
}
```

### 3. Test Triggers
**Endpoint for Scheduled:** `POST /test/scheduled/`  
**Payload:**  
```json
{
  "schedule_time": "2025-01-26T15:10:00"
}
```

**Endpoint for API:** `POST /test/api/`  
**Payload:**  
```json
{
  "payload": { "key": "value" }
}
```

## Local Setup

### Prerequisites
- Docker
- Docker Compose

### Steps
1. Clone the repository:  
   ```bash
   git clone <repository-link>
   cd event-trigger-platform
   ```

2. Build the Docker image:  
   ```bash
   docker-compose build
   ```

3. Run the application:  
   ```bash
   docker-compose up
   ```

4. Access the application:  
   - **Frontend:** `http://127.0.0.1:5500`  
   - **Backend:** `http://127.0.0.1:8000`

### Database Setup
The database schema is initialized automatically. If needed, you can reinitialize it by running:  
```bash
python initialize_database.py
```

---

## Running Tests
Tests can be run using the following command:  
```bash
pytest
```

---


## Cost Estimation
**Assumptions:**
- Hosted on Render (backend) and Vercel (frontend).  
- Queries: 5 queries/day.  

| Component             | Monthly Cost (USD) |
|-----------------------|--------------------|
| Render Free Tier      | Free               |
| Vercel Free Tier      | Free               |
| SQLite                | Free               |
| Total                 | 0 USD              |

---

## Notes
1. **Authentication:** Simple API key-based authentication is implemented. 
2. **Caching:** Event logs are cached using Redis for performance.
3. **Tools Used:**
   - Python (FastAPI)
   - SQLite (Database)
   - Redis (Caching)
   - Uvicorn (ASGI Server)
   - Render (Backend Hosting)
   - Vercel (Frontend Hosting)
   - ChatGPT
   - ClaudeAI
   - Postman

---

## Assumptions
1. Triggers can be edited but not paused once active.
2. Event logs are retained for exactly 48 hours (2 hours active + 46 hours archived).
3. Deployment uses free-tier resources for cost efficiency.

---
