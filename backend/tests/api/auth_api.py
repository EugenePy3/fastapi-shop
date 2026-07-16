class AuthApi:
    def __init__(self, client):
        self.client = client

    def register(self, name, password):
        return self.client.post(
            '/auth/register',
            json={
                'name': name,
                'password': password,
            }
        )

    def login(self, name, password):
        return self.client.post(
            '/auth/login',
            json={
                'name': name,
                'password': password,
            }
        )

    def logout(self):
        return self.client.post('/auth/logout')

    def me(self):
        return self.client.get('/auth/me')

