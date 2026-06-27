# Backend App

Simple FastAPI backend. Auth + Task management.

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Running the App
1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
2. Build and run the stack:
   ```bash
   docker compose up --build -d
   ```
3. The app is at `http://localhost:8080`.

## Features
- JWT Auth
- Task CRUD
- PostgreSQL integration
- Structured logging
