# 🚀 Task Manager API Backend

A personal best project, simple but effective REST API built with FastAPI and PostgreSQL. This backend handles secure user authentication and structured task management with full relational mapping.

---

##  Features

* **JWT Authentication:** Secure user signup and login protection using OAuth2 with JSON Web Tokens (JWT) and Bcrypt password hashing.
* **Task CRUD Operations:** relational Task management (Create, Read, Update, Delete) dynamically tied to authenticated user owners.
* **PostgreSQL Integration:** database storage utilizing modern SQLAlchemy 2.0 relational schemas.
* **Structured Logging:** Integrated system tracing via standard library logging to replace primitive prints with production-ready logs.

---

## 🛠️ Setup & Installation

### 1. Configuration (`.env`)
Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgres://db_name:your_password@localhost:5433/postgres
PROJECT_NAME="FastAPI Task Manager"
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
