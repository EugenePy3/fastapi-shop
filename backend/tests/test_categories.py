MISSING_CATEGORY_ID = 999999


def test_get_categories(category, categories_api):
    response = categories_api.list()
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c['id'] == category['id'] for c in data)


def test_get_category(category, categories_api):
    response = categories_api.get(category['id'])
    assert response.status_code == 200

    data = response.json()

    assert data['id'] == category['id']
    assert data['name'] == category['name']
    assert data['slug'] == category['slug']


def test_update_category(category, categories_api):
    response = categories_api.update(
        category['id'],
        name='updated Phones',
        slug='updated-phones',
    )
    assert response.status_code == 200
    get_category_response = categories_api.get(category['id'])
    assert get_category_response.status_code == 200

    data = get_category_response.json()

    assert data['name'] == 'updated Phones'
    assert data['slug'] == 'updated-phones'


def test_delete_category(category, categories_api):
    response = categories_api.delete(category['id'])
    assert response.status_code == 204

    get_category_response = categories_api.get(category['id'])
    assert get_category_response.status_code == 404


def test_create_duplicate_slug(categories_api):
    categories_api.create(name='Phones', slug='phones')
    response = categories_api.create(name='Phones 2', slug='phones')
    assert response.status_code == 409


def test_get_missing_category(categories_api):
    response = categories_api.get(MISSING_CATEGORY_ID)
    assert response.status_code == 404

    data = response.json()
    assert data['detail'] == f"Category with id '{MISSING_CATEGORY_ID}' not found."


def test_update_missing_category(categories_api):
    response = categories_api.update(
        category_id=MISSING_CATEGORY_ID,
        name='Updates Phones',
        slug='updates-phones',
    )
    assert response.status_code == 404

    data = response.json()
    assert data['detail'] == f"Category with id '{MISSING_CATEGORY_ID}' not found."


def test_delete_missing_category(categories_api):
    response = categories_api.delete(MISSING_CATEGORY_ID)
    assert response.status_code == 404

    data = response.json()
    assert data['detail'] == f"Category with id '{MISSING_CATEGORY_ID}' not found."


def test_delete_category_with_products(category, product, categories_api):
    response = categories_api.delete(category['id'])
    assert response.status_code == 409

    data = response.json()
    assert 'products still assigned' in data['detail']

    get_category_response = categories_api.get(category['id'])
    assert get_category_response.status_code == 200
