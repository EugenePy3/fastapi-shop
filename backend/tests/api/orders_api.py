class OrdersApi:
    def __init__(self, client):
        self.client = client

    def create(self):
        return self.client.post('/api/orders')

    def list(self):
        return self.client.get('/api/orders')

    def get_order(self, order_id):
        return self.client.get(f'/api/orders/{order_id}')

    def update_status(self, order_id, status):
        return self.client.patch(
            f'api/orders/{order_id}/status',
            json={
                'status': status,
            }
        )
