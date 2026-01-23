# Trader Cabinet API

Backend API for trading application and robot.

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL
- MinIO (S3-compatible storage)

### Installation

1.  **Clone the repository** (if valid).

2.  **Create virtual environment and install dependencies**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the project root with the following variables:

    ```env
    ENVIRONMENT=local
    DEBUG=True
    
    # Database
    DB_DSN=postgresql+asyncpg://user:password@localhost:port/db_name
    DB_ECHO=False
    
    # App Settings
    TZ=Europe/Moscow
    LOG_LEVEL=INFO
    SECRET_KEY=your_secret_key
    ENCRYPT_ALGORITHM=HS256
    
    # JWT Settings
    ACCESS_TOKEN_EXPIRE_DAYS=1
    REFRESH_TOKEN_EXPIRE_DAYS=15
    
    # CORS
    CORS_ALLOW_ORIGINS='["http://localhost:8000", "http://localhost:5173"]'  # for frontend development
    CORS_ALLOW_METHODS='["GET","POST","PUT","DELETE","OPTIONS"]'
    
    # MinIO Storage
    MINIO_ENDPOINT=localhost:9000
    MINIO_ACCESS_KEY=minioadmin
    MINIO_SECRET_KEY=minioadmin
    MINIO_BUCKET_NAME=trading-data
    MINIO_SECURE=False
    ```

4. Documentation: `http://localhost:8000/docs`.

## Layered architecture

-   **API Layer (`src/apis`)**: 
    -   Built with **FastAPI**.
    -   Handles HTTP requests, routing, and response formatting.
    -   `v1` router contains feature-specific endpoints (Auth, T-Tech API, Data).

-   **Core Layer (`src/core`)**:
    -   Contains business logic orchestration.
    -   Follows **CQRS** (Command Query Responsibility Segregation) pattern with `queries` and `commands` handlers.
    -   Example: `GetAllCandlesQuery` handles fetching and processing candle data.

-   **Domain Layer (`src/domain`)**:
    -   Defines the core business entities/models (`src/domain/models`).
    -   Contains interfaces and core services (e.g., `StorageService`, `EncryptionService`).
    -   Holds independent logic and enums.

-   **Data Access Layer (DAL) (`src/dal`)**:
    -   Handles interaction with the database and external APIs.
    -   **Fetchers**: Used to retrieve data from database (e.g., Tokens, Users).
    -   **Engines**: Asynchronous database engine configuration (SQLAlchemy).

### Stack
-   **Main web framework**: FastAPI
-   **DB**: PostgreSQL (Asyncpg + SQLAlchemy 2.0)
-   **Migrations**: Alembic
-   **File storage**: MinIO (via `minio` client)
-   **Validation**: Pydantic

## Data Integration

### T-Tech API
The application integrates with "Т-инвестиции" API to load historical market data.

**Implemented Features:**
-   **Candles**: Fetch generic historical candles for instruments.
    -   **Parameters**: `figi` (Instrument ID), `interval` (1min to 1month), Time range (Years/Weeks/Days).
    -   **Output**: Data is processed (Open/Close/High/Low/Volume) and saved as **CSV** files in MinIO storage.
    -   **Calculated Fields**: `IsGrowing`, `AvgOpenClose`, `DiffOpenClose`, `DiffHighLow`.

### MOEX API
*Currently not implemented.*
Future plans include integrating with MOEX (Moscow Exchange) ISS API to fetch additional Russian market data.

---

## Trading Robot

*(This section is currently empty. Trading algorithms and robot logic are to be implemented.)*
