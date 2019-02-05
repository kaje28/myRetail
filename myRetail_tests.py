import json
import pytest
import myRetail

@pytest.fixture
def client(request):
    test_client = myRetail.app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client

def test_collection(mongodb):
    assert 'itemPriceInfo' in mongodb.collection_names()

def test_valid_product_id(client):
    response = client.get('/products/51591640')
    assert b'ProductRetailPrice' in response.data

def test_bad_product_id(client):
    response = client.get('/products/11111111')
    assert b'Valid Product ID not entered' in response.data
