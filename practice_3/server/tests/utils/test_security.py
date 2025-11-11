from datetime import timedelta, datetime, timezone
from app.utils.security import create_access_token, verify_password, get_password_hash
from app.utils.config import settings
import jwt


def test_password_hashing_and_verification():
    password = "user123"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("user321", hashed_password) is False
    assert hashed_password != password


def test_different_hashes_for_same_password():
    password = "admin123"
    hashed_password1 = get_password_hash(password)
    hashed_password2 = get_password_hash(password)

    assert hashed_password1 != hashed_password2
    assert verify_password(password, hashed_password1) is True
    assert verify_password(password, hashed_password2) is True


def test_create_access_token():
    data = {"sub": "user", "user_id": 1}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "user"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

    exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    assert 14 <= (exp_time - now).total_seconds() / 60 <= 16


def test_create_access_token_with_expires_delta():
    data = {"sub": "user", "user_id": 1}
    expires_delta = timedelta(hours=2)

    token = create_access_token(data, expires_delta=expires_delta)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded["sub"] == "user"
    assert decoded["user_id"] == 1
    assert "exp" in decoded

    exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    assert 119 <= (exp_time - now).total_seconds() / 60 <= 121
