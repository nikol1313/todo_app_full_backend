# Backend App

Simple FastAPI backend. Auth + Task management.

## Setup
1. Create `.env`:
   ```
   DATABASE_URL=postgresql://user:pass@localhost:5432/db
   PROJECT_NAME=backendapp
   SECRET_KEY=yoursecret
   ```
2. Install dependencies + run:
   ```bash
   uvicorn main:app --reload
   ```

## Features
- JWT Auth
- Task CRUD
- PostgreSQL integration
- Structured logging
