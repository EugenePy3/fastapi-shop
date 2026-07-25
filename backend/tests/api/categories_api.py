class CategoriesApi:
    def __init__(self, client):
        self.client = client

    def list(self):
        return self.client.get('/api/categories')

    def get(self, category_id):
        return self.client.get(f'/api/categories/{category_id}')

    def create(self, name, slug):
        return self.client.post(
            '/api/categories',
            json={
                'name': name,
                'slug': slug,
            }
        )

    def update(self, category_id, name, slug):
        return self.client.patch(
            f'/api/categories/{category_id}',
            json={
                'name': name,
                'slug': slug,
            }
        )

    def delete(self, category_id):
        return self.client.delete(
            f'/api/categories/{category_id}'
        )
