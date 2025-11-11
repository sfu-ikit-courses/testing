import pytest
from unittest.mock import MagicMock
from app.crud import role as crud
from app.models.user import Role, Permission
from app.schemas.user import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate


# Fixtures
@pytest.fixture
def db_session():
    return MagicMock()


@pytest.fixture
def sample_role():
    return Role(id=1, name="admin", permissions=[])


@pytest.fixture
def sample_permission():
    return Permission(id=1, name="read")


# Role Tests
def test_create_role(db_session):
    role_in = RoleCreate(name="admin")
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    db_session.refresh = MagicMock()

    role = crud.create_role(db_session, role_in)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(role)
    assert role.name == "admin"


def test_get_role(db_session, sample_role):
    db_session.query().filter().first.return_value = sample_role
    role = crud.get_role(db_session, 1)
    assert role == sample_role


def test_get_role_by_name(db_session, sample_role):
    db_session.query().filter().first.return_value = sample_role
    role = crud.get_role_by_name(db_session, "admin")
    assert role == sample_role


def test_update_role(db_session, sample_role):
    db_session.query().filter().first.return_value = sample_role
    role_update = RoleUpdate(name="moderator")

    updated_role = crud.update_role(db_session, 1, role_update)

    assert updated_role.name == "moderator"
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(sample_role)


def test_delete_role(db_session, sample_role):
    db_session.query().filter().first.return_value = sample_role

    result = crud.delete_role(db_session, 1)

    db_session.delete.assert_called_once_with(sample_role)
    db_session.commit.assert_called_once()
    assert result is True


def test_get_all_roles(db_session, sample_role):
    db_session.query().offset().limit().all.return_value = [sample_role]
    roles = crud.get_all_roles(db_session, skip=0, limit=10)
    assert roles == [sample_role]


# Permission Tests
def test_create_permission(db_session):
    perm_in = PermissionCreate(name="read")
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    db_session.refresh = MagicMock()

    perm = crud.create_permission(db_session, perm_in)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(perm)
    assert perm.name == "read"


def test_get_permission(db_session, sample_permission):
    db_session.query().filter().first.return_value = sample_permission
    perm = crud.get_permission(db_session, 1)
    assert perm == sample_permission


def test_update_permission(db_session, sample_permission):
    db_session.query().filter().first.return_value = sample_permission
    perm_update = PermissionUpdate(name="write")

    updated_perm = crud.update_permission(db_session, 1, perm_update)

    assert updated_perm.name == "write"
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(sample_permission)


def test_delete_permission(db_session, sample_permission):
    db_session.query().filter().first.return_value = sample_permission

    result = crud.delete_permission(db_session, 1)

    db_session.delete.assert_called_once_with(sample_permission)
    db_session.commit.assert_called_once()
    assert result is True


def test_get_all_permissions(db_session, sample_permission):
    db_session.query().offset().limit().all.return_value = [sample_permission]
    perms = crud.get_all_permissions(db_session, skip=0, limit=10)
    assert perms == [sample_permission]


# Role-Permission Association Tests
def test_add_permission_to_role(db_session, sample_role, sample_permission):
    db_session.commit = MagicMock()
    db_session.refresh = MagicMock()

    updated_role = crud.add_permission_to_role(
        db_session, sample_role, sample_permission
    )

    assert sample_permission in updated_role.permissions
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(sample_role)


def test_remove_permission_from_role(db_session, sample_role, sample_permission):
    sample_role.permissions.append(sample_permission)
    db_session.commit = MagicMock()
    db_session.refresh = MagicMock()

    updated_role = crud.remove_permission_from_role(
        db_session, sample_role, sample_permission
    )

    assert sample_permission not in updated_role.permissions
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(sample_role)
