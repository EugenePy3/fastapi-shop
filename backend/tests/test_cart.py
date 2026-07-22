def test_empty_cart(cart_api):
    response = cart_api.get_cart()
    assert response.status_code == 200

    data = response.json()

    assert data['items'] == []
    assert data['total'] == 0


def test_add_product_to_cart(cart_api, product):
    response = cart_api.add_to_cart(
        product['id'],
        quantity=2,
    )
    assert response.status_code == 200

    cart = cart_api.get_cart().json()

    assert len(cart['items'] == 1)
    assert cart['items'][0]['product_id'] == product['id']
    assert cart["items"][0]["quantity"] == 2
    assert cart['total'] == product['price'] * 2


def test_update_product_quantity(cart_api, product):
    cart_api.add_to_cart(
        product['id'],
        quantity=1,
    )
    response = cart_api.update_cart_item(
        product['id'],
        quantity=5,
    )
    assert response.status_code == 200

    cart = cart_api.get_cart().json()

    assert len(cart['items']) == 1
    assert cart['items'][0]['quantity'] == 5
    assert cart['total'] == product['price'] * 5


def test_remove_product_from_cart(cart_api, product):
    cart_api.add_to_cart(
        product['id'],
        quantity=2,
    )
    response = cart_api.remove_cart_item(
        product['id'],
    )
    assert response.status_code == 204

    cart = cart_api.get_cart().json()

    assert cart['items'] == []
    assert cart['total'] == 0


def test_clear_cart(cart_api, product):
    cart_api.add_to_cart(
        product['id'],
        quantity=2,
    )

    response = cart_api.clear_cart()

    assert response.status_code == 204

    cart = cart_api.get_cart().json()

    assert cart['items'] == []
    assert cart['total'] == 0


def test_add_same_product_twice(cart_api, product):
    cart_api.add_to_cart(product["id"], quantity=1)
    cart_api.add_to_cart(product["id"], quantity=2)

    cart = cart_api.get_cart().json()

    assert len(cart['items']) == 1
    assert cart['items'][0]['quantity'] == 3


def test_remove_missing_product(cart_api):
    response = cart_api.remove_cart_item(999)
    assert response.status_code == 404
