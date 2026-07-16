def test_register_success(auth_api, user_data):
    response = auth_api.register(**user_data)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == user_data['name']
    assert isinstance(data['id'], int)


def test_register_duplicate_user(auth_api, registered_user):
    response = auth_api.register(**registered_user)
    assert response.status_code == 409
    data = response.json()
    assert data['detail'] == 'User already exists.'


def test_login_success(auth_api, registered_user):
    response = auth_api.login(**registered_user)
    assert response.status_code == 200
    data = response.json()
    assert data['user']['id'] > 0
    assert data['user']['name'] == registered_user['name']
    assert response.cookies.get('session_id') is not None


def test_login_invalid_password(auth_api, registered_user):
    response = auth_api.login(
            name=registered_user['name'],
            password='wrong_password')

    assert response.status_code == 401
    data = response.json()
    assert data['detail'] == 'Invalid username or password.'
    assert response.cookies.get('session_id') is None


def test_logout(authenticated_api):
    response = authenticated_api.logout()
    assert response.status_code == 200
    data = response.json()
    assert data['detail'] == 'Logged out...'
    assert response.cookies.get('session_id') is None


def test_me_returns_current_user(authenticated_api, registered_user):
    response = authenticated_api.me()
    assert response.status_code == 200
    data = response.json()
    assert data['id'] > 0
    assert data['name'] == registered_user['name']


def test_session_lifecycle(auth_api, registered_user):
    login_response = auth_api.login(**registered_user)
    assert login_response.status_code == 200
    assert login_response.cookies.get('session_id') is not None

    me_response = auth_api.me()
    assert me_response.status_code == 200
    assert me_response.json()['name'] == registered_user['name']

    logout_response = auth_api.logout()
    assert logout_response.status_code == 200

    me_response_after_logout = auth_api.me()
    assert me_response_after_logout.status_code == 401
