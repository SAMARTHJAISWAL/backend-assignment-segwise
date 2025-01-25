# Event Trigger Platform

## Overview
The Event Trigger Platform is a robust system designed to create, manage, and test triggers and events. Built with FastAPI for APIs, Redis for caching, and SQLite for persistent storage, it prioritizes modularity, scalability, and simplicity.

---

## Features
- **Trigger Management:** Create, read, update, and delete triggers.
- **Event Logging:** Logs all events, including manual and automated triggers.
- **Caching:** Optimized with Redis for high-performance reads of event logs.
- **Scheduled Cleanup:** Automatically removes logs older than 48 hours.
- **Pagination:** Fetch event logs efficiently with pagination support.
- **Aggregation:** Aggregate logs by `trigger_id` for insights and analytics.
- **Authentication:** Secured with API key-based authentication.
- **Dockerized Environment:** Simplified setup and deployment using Docker.

---

## Requirements
- Python 3.10+
- FastAPI
- Redis
- Docker (optional for containerized deployment)

---

## Installation

### Local Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd event-trigger-platform
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Redis server:
   ```bash
   redis-server
   ```

5. Initialize the SQLite database:
   ```bash
   python initialize_database.py
   ```

6. (Optional) Populate the database with sample data:
   ```bash
   python populate_events.py
   ```

### Run the Application
1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open the Swagger UI for API documentation:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Using Docker

1. Build and start the application with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Verify services:
   - Backend: [http://localhost:8000](http://localhost:8000)
   - Frontend: [http://localhost:5500](http://localhost:5500)
   - Redis: `localhost:6379`

3. Stop and clean up:
   ```bash
   docker-compose down
   ```

---

## API Endpoints

### Triggers
- `POST /triggers/` - Create a new trigger.
- `GET /triggers/` - List all triggers.
- `PUT /triggers/{id}` - Update an existing trigger.
- `DELETE /triggers/{id}` - Delete a trigger.

### Events
- `GET /events/` - List event logs with pagination.
- `GET /events/aggregate` - Aggregate logs by `trigger_id`.
- `PUT /events/archive/{id}` - Archive an event.

### Testing
- `POST /test/` - Manually test a trigger.

---

## Environment Variables
Create a `.env` file in the root directory with the following:
```env
X_API_KEY=your-secure-secret-key-123456
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## Deployment

### Docker Deployment
1. Build the Docker image:
   ```bash
   docker build -t event-trigger-platform .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 event-trigger-platform
   ```

### Cloud Deployment
The platform can be deployed on cloud platforms such as AWS, Azure, or Heroku using containerized or virtualized setups. CI/CD integration is recommended for streamlined deployments.

---

## Future Enhancements
- Develop a web-based UI for managing triggers and events.
- Add real-time analytics dashboards and advanced reporting.
- Implement multi-database support (e.g., PostgreSQL, MySQL).
- Extend cloud compatibility for AWS Lambda or Azure Functions.

---