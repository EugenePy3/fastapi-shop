def test_register_success(client):
    response = client.post(
        '/auth/register',
        json={
            "name": 'Eugen',
            "password": '12345678',
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data['name'] == 'Eugen'
    assert isinstance(data['id'], int)


def test_register_duplicate_user(client):
    client.post(
        '/auth/register',
        json={
            'name': 'Eugen',
            'password': '12345678'
        },
    )

    response = client.post(
        '/auth/register',
        json={
            "name": 'Eugen',
            "password": '12345678',
        },
    )
    assert response.status_code == 409
    data = response.json()

    assert data['detail'] == 'User already exists'


def test_login_success(client):
    client.post(
        '/auth/register',
        json={
            "name": 'Eugen',
            "password": '12345678',
        },
    )

    response = client.post(
        '/auth/login',
        json={
            "name": 'Eugen',
            "password": '12345678',
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data['user']['id'] > 0
    assert data['user']['name'] == 'Eugen'
    assert response.cookies.get('session_id') is not None


def test_login_invalid_password(client):
    client.post(
        '/auth/register',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    response = client.post(
        '/auth/login',
        json={
            'name': 'Eugen',
            'password': 'wrong_password',
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data['detail'] == 'Invalid username or password.'
    assert response.cookies.get('session_id') is None


def test_logout(client):
    client.post(
        '/auth/register',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    login_response = client.post(
        '/auth/login',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    assert login_response.cookies.get('session_id') is not None

    response = client.post('/auth/logout')

    assert response.status_code == 200

    data = response.json()

    assert data['detail'] == 'Logged out...'
    assert response.cookies.get('session_id') == ''


def test_me_session(client):
    client.post(
        '/auth/register',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    client.post(
        '/auth/login',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    response = client.get('/auth/me')

    assert response.status_code == 200

    data = response.json()

    assert data['id'] > 0
    assert data['name'] == 'Eugen'


def test_session_lifecycle(client):
    client.post(
        '/auth/register',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    login_response = client.post(
        '/auth/login',
        json={
            'name': 'Eugen',
            'password': '12345678',
        },
    )

    assert login_response.status_code == 200
    assert login_response.cookies.get('session_id') is not None

    me_response = client.get('/auth/me')

    assert me_response.status_code == 200
    assert me_response.json()['name'] == 'Eugen'

    logout_response = client.post('/auth/logout')

    assert logout_response.status_code == 200

    me_response_after_logout = client.get('/auth/me')

    assert me_response_after_logout.status_code == 401
