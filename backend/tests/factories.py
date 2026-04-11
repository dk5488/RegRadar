import factory
from faker import Faker
from app.models.models import User
from app.models.enums import UserRole
import uuid
import datetime

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = "hashed_default_password"  # Bypass slow bcrypt hashing for tests
    full_name = factory.Faker("name")
    phone = "9999999999"
    role = UserRole.MSME_OWNER
    is_active = True
    is_verified = True
    created_at = factory.LazyFunction(datetime.datetime.now)
    updated_at = factory.LazyFunction(datetime.datetime.now)
