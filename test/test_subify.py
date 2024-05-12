"""Imports"""
import pytest
import subify.models as models
from subify import database, create_app
from werkzeug.security import generate_password_hash


# Setup phase
@pytest.fixture()
def setup_subify():
    """Setup subify for testing"""
    app = create_app('sqlite:///test.db')
    app.config.from_mapping({
        "TESTING": True
    })

    with app.app_context():
        database.create_all()

    return app


@pytest.fixture
def setup_user(setup_subify):
    """Setup user for testing"""

    with setup_subify.app_context():
        user = models.User(
            email='test@test.com',
            name='testtest',
            password=generate_password_hash('testtest')
        )
        database.session.add(user)
        return user


@pytest.fixture
def setup_subs(setup_subify):
    """Setup expenses for testing"""

    with setup_subify.app_context():
        sub = models.Sub(
            name='test',
            type='streaming',
            occurance_type='monthly',
            price=2000,
            is_paid=False
        )
        database.session.add(sub)
        return sub


@pytest.fixture
def setup_client(setup_subify):
    """Client setup for testing"""

    return setup_subify.test_client()


# Test phase
def test_index(setup_client):
    """Test main.index endpoint"""

    response = setup_client.get('/')
    assert response.status_code == 200
    assert b'content="Nicewithothers"' in response.data


def test_unauthorized(setup_client):
    """Test anonymous user endpoint"""

    response = setup_client.get('/dashboard')
    assert response.status_code == 401


def test_register(setup_subify, setup_client):
    """Test register endpoint"""

    response = setup_client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

    post_data = {
        'email': 'test@test.com',
        'name': 'test',
        'password': 'testtest',
        'password_verify': 'testtest'
    }

    response = setup_client.post('/register', data=post_data, follow_redirects=True)
    assert response.status_code == 200

    with setup_subify.app_context():
        assert database.session.query(models.User).count() == 1

    post_data = {
        'email': 'test',
        'name': 'test',
        'password': 'testtest',
        'password_verify': 'testtest'
    }

    response = setup_client.post('/register', data=post_data)
    assert response.status_code == 200
    assert b'Invalid email format!' in response.data

    post_data = {
        'email': 'test@test.com',
        'name': 'test',
        'password': 'teszt',
        'password_verify': 'testtezst'
    }

    response = setup_client.post('/register', data=post_data)
    assert response.status_code == 200
    assert b'Passwords do not match!' in response.data


def test_login(setup_client, setup_user):
    """Test login endpoint"""

    response = setup_client.get('/login')
    assert response.status_code == 200

    post_data = {
        'email': 'test@test.com',
        'password': 'testtest'
    }

    response = setup_client.post('/login', data=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert '/dashboard' in response.request.path

