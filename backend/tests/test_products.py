from decimal import Decimal

MISSING_PRODUCT_ID = 999999
MISSING_CATEGORY_ID = 999999


def test_get_products(product, products_api):
    response = products_api.list()
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data['products'], list)
    assert len(data['products']) >= 1
    assert any(p['id'] == product['id'] for p in data['products'])


def test_get_product(category, product, products_api):
    response = products_api.get(product['id'])
    assert response.status_code == 200

    data = response.json()

    assert data['id'] == product['id']
    assert data['name'] == product['name']
    assert data['description'] == product['description']
    assert Decimal(data['price']) == Decimal(product['price'])
    assert data['category_id'] == category['id']
    assert data['image_url'] == product['image_url']


def test_update_product(product, products_api):
    response = products_api.update(
        product['id'],
        name='new_name',
        description='new_description',
        price=999,
        category_id=product['category_id'],
        image_url='new_image',
    )
    assert response.status_code == 200

    update = response.json()
    assert update['name'] == 'new_name'

    get_product_response = products_api.get(product['id'])
    assert get_product_response.status_code == 200

    data = get_product_response.json()

    assert data['name'] == 'new_name'
    assert data['description'] == 'new_description'
    assert Decimal(data['price']) == Decimal('999')
    assert data['category_id'] == product['category_id']
    assert data['image_url'] == 'new_image'


def test_update_product_category(
        product,
        products_api,
        categories_api,
):
    new_category = categories_api.create(
        name='Laptops',
        slug='laptops'
    ).json()

    response = products_api.update(
        product['id'],
        name=product['name'],
        description=product['description'],
        price=product['price'],
        category_id=new_category['id'],
        image_url=product['image_url'],
    )
    assert response.status_code == 200

    updated = response.json()

    assert updated['category_id'] == new_category['id']
    assert updated['category']['id'] == new_category['id']

    assert updated["name"] == product["name"]
    assert updated["description"] == product["description"]
    assert Decimal(updated["price"]) == Decimal(product["price"])
    assert updated["image_url"] == product["image_url"]


def test_delete_product(product, products_api):
    response = products_api.delete(product['id'])
    assert response.status_code == 204

    get_product_response = products_api.get(product['id'])
    assert get_product_response.status_code == 404


def test_get_missing_product(products_api):
    response = products_api.get(MISSING_PRODUCT_ID)
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Product with id '{MISSING_PRODUCT_ID}' not found."


def test_update_missing_product(category, products_api):
    response = products_api.update(
        MISSING_PRODUCT_ID,
        name='Updated',
        description='Updated description',
        price=500,
        category_id=category['id'],
        image_url=None,
    )
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Product with id '{MISSING_PRODUCT_ID}' not found."


def test_update_product_to_missing_category(product, products_api):
    response = products_api.update(
        product['id'],
        name=product['name'],
        description=product['description'],
        price=product['price'],
        category_id=MISSING_CATEGORY_ID,
        image_url=product['image_url'],
    )
    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == (
        f"Category with id '{MISSING_CATEGORY_ID}' not found."
    )


def test_delete_missing_product(products_api):
    response = products_api.delete(MISSING_PRODUCT_ID)
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Product with id '{MISSING_PRODUCT_ID}' not found."


def test_create_product_with_missing_category(products_api):
    response = products_api.create(
        name="iPhone",
        description="Test",
        price=1000,
        category_id=MISSING_CATEGORY_ID,
        image_url=None,
    )
    assert response.status_code == 404

    data = response.json()

    assert data['detail'] == f"Category with id '{MISSING_CATEGORY_ID}' not found."


def test_create_product_negative_price(category, products_api):
    response = products_api.create(
        name='iPhone',
        description='Test',
        price=-1000,
        category_id=category['id'],
        image_url=None,
    )

    assert response.status_code == 422


def test_create_product_zero_price(category, products_api):
    response = products_api.create(
        name='iPhone',
        description='Test',
        price=0,
        category_id=category['id'],
        image_url=None,
    )

    assert response.status_code == 422


def test_create_product_empty_name(category, products_api):
    response = products_api.create(
        name='',
        description='Test',
        price=1000,
        category_id=category['id'],
        image_url=None,
    )

    assert response.status_code == 422
