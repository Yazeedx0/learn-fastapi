# FastAPI User Management API

A production-ready FastAPI application with user authentication, role-based access control, and best practices implementation.

## Features

- ✅ User registration and authentication
- ✅ JWT-based access and refresh tokens
- ✅ Role-based access control (RBAC)
- ✅ Password strength validation
- ✅ Rate limiting
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Alembic database migrations
- ✅ CORS middleware
- ✅ Logging and error handling
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Docker support

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Jose** - JWT token handling
- **Passlib** - Password hashing
- **SlowAPI** - Rate limiting

## Setup Instructions

### 1. Clone the Repository

\`\`\`bash
git clone <repository-url>
cd learn-fastapi
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment Variables

\`\`\`bash
cp .env.example .env
\`\`\`

Edit \`.env\` and set your values:
\`\`\`env
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db
SECRET_KEY=your-super-secret-key-change-this
\`\`\`

Generate a secure secret key:
\`\`\`bash
openssl rand -hex 32
\`\`\`

### 5. Run the Application

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

The API will be available at \`http://localhost:8000\`

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Authentication
- \`POST /api/v1/auth/login\` - Login and get access/refresh tokens
- \`GET /api/v1/auth/admin-only\` - Admin-only test endpoint

### Users
- \`POST /api/v1/users/register\` - Register a new user
- \`GET /api/v1/users/me\` - Get current user info

### Health
- \`GET /\` - Root endpoint
- \`GET /health\` - Health check

## Security Best Practices Implemented

1. **Password Security**
   - Minimum 8 characters
   - Requires uppercase, lowercase, digit, and special character
   - Bcrypt hashing with salt

2. **JWT Tokens**
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (10 days)
   - Token type validation

3. **API Security**
   - Rate limiting (5 requests/minute for login)
   - CORS configuration
   - Input validation with Pydantic
   - Role-based access control

4. **Error Handling**
   - Centralized error handling
   - Logging for debugging

## Common Issues Fixed

1. ✅ Typos (from_data → form_data, oath2 → oauth2, etc.)
2. ✅ Token creation fixed to use proper parameters
3. ✅ Role comparison fixed in authorization
4. ✅ Timezone issues resolved
5. ✅ Password validation added
6. ✅ Logging added throughout
7. ✅ Type hints improved
8. ✅ Documentation added

## License

MIT
