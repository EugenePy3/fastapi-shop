from decimal import Decimal

from app.enums.order_status import OrderStatus

MISSING_ORDER_ID = 999999


def test_create_order(cart_with_product, cart_api, orders_api):
    response = orders_api.create()
    assert response.status_code == 201

    data = response.json()

    assert data['id'] > 0
    assert data['status'] == 'pending'

    assert len(data['items']) == 1

    expected = cart_with_product
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


def test_get_order(order, cart_with_product, orders_api):
    response = orders_api.get_order(order['id'])
    assert response.status_code == 200

    data = response.json()

    received_item = data['items'][0]

    assert data['id'] == order['id']
    assert data['status'] == order['status']
    assert Decimal(data['total_amount']) == Decimal(order['total_amount'])

    assert received_item['product_id'] == cart_with_product['product_id']
    assert received_item['product_name'] == cart_with_product['product_name']
    assert Decimal(received_item['product_price']) == Decimal(cart_with_product['product_price'])
    assert received_item['quantity'] == cart_with_product['quantity']
    assert Decimal(received_item['subtotal']) == Decimal(cart_with_product['subtotal'])


def test_get_orders(order, orders_api):
    response = orders_api.list()
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data['orders'], list)
    assert len(data['orders']) == 1
    assert any(o['id'] == order['id'] for o in data['orders'])

    returned_order = data['orders'][0]

    assert returned_order['id'] == order['id']
    assert returned_order['status'] == order['status']
    assert Decimal(returned_order['total_amount']) == Decimal(order['total_amount'])


def test_get_missing_order(orders_api):
    response = orders_api.get_order(MISSING_ORDER_ID)
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Order with id '{MISSING_ORDER_ID}' not found."


def test_user_cannot_get_another_users_order(admin_order, orders_api):
    response = orders_api.get_order(admin_order['id'])
    assert response.status_code == 403

    data = response.json()

    assert data['detail'] == 'You do not have access to this order.'


def test_get_orders_returns_only_current_user_orders(
    orders_api,
    order,
    admin_order,
):
    response = orders_api.list()
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data['orders'], list)

    ids = [o['id'] for o in data['orders']]

    assert order['id'] in ids
    assert admin_order['id'] not in ids


def test_update_order_status(order, admin_orders_api):
    response = admin_orders_api.update_status(order['id'], 'paid')
    assert response.status_code == 200

    data = response.json()

    assert data['status'] == 'paid'


def test_update_missing_order_status(admin_orders_api):
    response = admin_orders_api.update_status(
        MISSING_ORDER_ID,
        status=OrderStatus.PAID.value,
    )
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Order with id '{MISSING_ORDER_ID}' not found."


def test_user_cannot_update_order_status(order, orders_api):
    response = orders_api.update_status(
        order['id'],
        status=OrderStatus.PAID.value,
    )
    assert response.status_code == 403

    data = response.json()

    assert data['detail'] == 'Admins only'


