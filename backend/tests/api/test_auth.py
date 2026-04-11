import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.core.security import hash_password

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio

async def test_register_user(async_client: AsyncClient, db_session: AsyncSession):
    """Test user registration endpoint."""
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword123",
            "full_name": "New User",
            "role": "msme_owner"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data

async def test_login_for_access_token(async_client: AsyncClient, db_session: AsyncSession):
    """Test login endpoint to acquire JWT."""
    # First, register and insert a known user
    user = User(
        email="loginuser@example.com",
        hashed_password=hash_password("securepassword123"),
        full_name="Login User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()

    # Attempt to login
    response = await async_client.post(
        "/api/v1/auth/token",
        data={
            "username": "loginuser@example.com",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
