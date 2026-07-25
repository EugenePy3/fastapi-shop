from decimal import Decimal


def test_empty_cart(cart_api):
    response = cart_api.get()
    assert response.status_code == 200

    data = response.json()

    assert data['items'] == []
    assert Decimal(data['total']) == Decimal('0')


def test_add_product_to_cart(cart_api, product):
    response = cart_api.add(
        product['id'],
        quantity=2,
    )
    assert response.status_code == 200

    cart = cart_api.get().json()

    assert len(cart['items']) == 1
    assert cart['items'][0]['product_id'] == product['id']
    assert cart["items"][0]["quantity"] == 2
    price = Decimal(product['price'])
    assert Decimal(cart['total']) == price * 2


def test_update_product_quantity(cart_api, product):
    cart_api.add(
        product['id'],
        quantity=1,
    )
    response = cart_api.update(
        product['id'],
        quantity=5,
    )
    assert response.status_code == 200

    cart = cart_api.get().json()

    assert len(cart['items']) == 1
    assert cart['items'][0]['quantity'] == 5
    price = Decimal(product['price'])
    assert Decimal(cart['total']) == price * 5


def test_remove_product_from_cart(cart_api, product):
    cart_api.add(
        product['id'],
        quantity=2,
    )
    response = cart_api.remove(
        product['id'],
    )
    assert response.status_code == 204

    cart = cart_api.get().json()

    assert cart['items'] == []
    assert Decimal(cart['total']) == Decimal('0')


def test_clear_cart(cart_api, product):
    cart_api.add(
        product['id'],
        quantity=2,
    )
    response = cart_api.clear()
    assert response.status_code == 204

    cart = cart_api.get().json()

    assert cart['items'] == []
    assert Decimal(cart['total']) == Decimal('0')


def test_add_same_product_twice(cart_api, product):
    cart_api.add(product["id"], quantity=1)
    cart_api.add(product["id"], quantity=2)

    cart = cart_api.get().json()

    assert len(cart['items']) == 1
    assert cart['items'][0]['quantity'] == 3


def test_remove_missing_product(cart_api):
    response = cart_api.remove(999)
    assert response.status_code == 404



