class ProductsApi:
    def __init__(self, client):
        self.client = client

    def list(self):
        return self.client.get('/api/products')

    def get(self, product_id):
        return self.client.get(f'/api/products/{product_id}')

    def by_category(self, category_id):
        return self.client.get(f'/api/products/category/{category_id}')

    def create(self, name, description, price, category_id, image_url):
        return self.client.post(
            '/api/products',
            json={
                'name': name,
                'description': description,
                'price': price,
                'category_id': category_id,
                'image_url': image_url,
            }
        )

    def update(self, product_id, name, description, price, category_id, image_url):
        return self.client.patch(
            f'/api/products{product_id}',
            json={
                'name': name,
                'description': description,
                'price': price,
                'category_id': category_id,
                'image_url': image_url,
            }
        )

    def delete(self, product_id):
        return self.client.delete(f'/api/products/{product_id}')

