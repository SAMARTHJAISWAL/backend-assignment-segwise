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
- Docker

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

## Future Enhancements
- Develop a web-based UI for managing triggers and events.
- Add real-time analytics dashboards and advanced reporting.
- Implement multi-database support (e.g., PostgreSQL, MySQL).
- Extend cloud compatibility for AWS Lambda or Azure Functions.
