from decimal import Decimal

MISSING_ORDER_ID = 999999


def test_create_order(cart_item, cart_api, orders_api):
    response = orders_api.create()
    assert response.status_code == 201

    data = response.json()

    assert data['id'] > 0
    assert data['status'] == 'pending'

    assert len(data['items']) == 1

    expected = cart_item
    item = data['items'][0]

    assert item['product_id'] == expected['product_id']
    assert item['product_name'] == expected['product_name']
    assert Decimal(item['product_price']) == expected['product_price']
    assert item['quantity'] == expected['quantity']
    assert Decimal(item['subtotal']) == expected['subtotal']


def test_create_order_without_cart(orders_api):
    response = orders_api.create()
    assert response.status_code == 404

    data = response.json()

    assert 'not found' in data['detail'].lower()


def test_get_all_orders(order, admin_orders_api):
    response = admin_orders_api.list()
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data['orders'], list)
    assert any(o['id'] == order['id'] for o in data['orders'])


def test_get_order(order, orders_api):
    response = orders_api.get_order(order['id'])
    assert response.status_code == 200

    data = response.json()

    created_item = order['items'][0]
    received_item = data['items'][0]

    assert data['id'] == order['id']
    assert data['status'] == order['status']

    assert Decimal(data['total_amount']) == Decimal(order['total_amount'])

    assert received_item['product_id'] == created_item['product_id']
    assert received_item['product_name'] == created_item['product_name']
    assert Decimal(received_item['product_price']) == Decimal(created_item['product_price'])
    assert received_item['quantity'] == created_item['quantity']
    assert Decimal(received_item['subtotal']) == Decimal(created_item['subtotal'])


def test_get_missing_order(orders_api):
    response = orders_api.get_order(MISSING_ORDER_ID)
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Order with id '{MISSING_ORDER_ID}' not found."



