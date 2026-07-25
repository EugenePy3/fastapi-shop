class CartApi:
    def __init__(self, client):
        self.client = client

    def get(self):
        return self.client.get('/api/cart')

    def add(self, product_id, quantity=1):
        return self.client.post(
            '/api/cart/items',
            json={
                'product_id': product_id,
                'quantity': quantity,
            }
        )

    def update(self, product_id, quantity):
        return self.client.patch(
            f'/api/cart/items/{product_id}',
            json={
                'quantity': quantity,
            }
        )

    def remove(self, product_id):
        return self.client.delete(f'/api/cart/items/{product_id}')

    def clear(self):
        return self.client.delete('/api/cart')
