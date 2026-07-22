class CartApi:
    def __init__(self, client):
        self.client = client

    def get_cart(self):
        return self.client.get('/cart')

    def add_to_cart(self, product_id, quantity=1):
        return self.client.post(
            '/cart/items',
            json={
                'product_id': product_id,
                'quantity': quantity,
            }
        )

    def update_cart_item(self, product_id, quantity):
        return self.client.patch(
            f'/cart/items/{product_id}',
            json={
                'quantity': quantity,
            }
        )

    def remove_cart_item(self, product_id):
        return self.client.delete(f'/items/{product_id}')

    def clear_cart(self):
        return self.client.delete('/cart')
