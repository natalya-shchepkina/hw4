import random

import pytest
import requests

import config

from jsonschema import validate
from src.base_request import BaseRequest

url = config.BASE_URL_BREW
base_request = BaseRequest(url)


def test_get_breweries():
    response = base_request.get('b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0')

    schema = {
        "type": "object",
        "properties": {
            "address_1": {"type": "string"},
            "brewery_type": {"type": "string"},
            "city": {"type": "string"},
            "country": {"type": "string"},
            "id": {"type": "string"},
            "latitude": {"type": "string"},
            "longitude": {"type": "string"},
            "name": {"type": "string"},
            "phone": {"type": "string"},
            "postal_code": {"type": "string"},
            "state": {"type": "string"},
            "state_province": {"type": "string"},
            "street": {"type": "string"},
            "website_url": {"type": "string"},
        },
        "required": ["id", "address_1", "country", "city"]
    }

    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize('type', ['micro', 'large', 'proprietor', 'closed'])
def test_filtration_by_type(type):
    response = requests.get('https://api.openbrewerydb.org/v1/breweries', params={'by_type': type})
    response = response.json()
    random_number = random.randint(1, 20)
    assert response[random_number]['brewery_type'] == type


@pytest.mark.parametrize('type', [-1, 0, 11, ''])
def test_filtration_by_type_negative(type):
    response = requests.get('https://api.openbrewerydb.org/v1/breweries', params={'by_type': type})

    assert response.json() == {'errors':
                                   ['Brewery type must include one of these types: '
                                   '["micro", "nano", "regional", "brewpub", "large", '
                                   '"planning", "bar", "contract", "proprietor", "closed"]'
                                    ]
                               }


def test_get_meta():
    schema = {
        "type": "object",
        "properties": {
            "total": {"type": "string"},
            "page": {"type": "string"},
            "per_page": {"type": "string"}
        }
    }
    response = base_request.get('meta')


    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize('endpoint', [
    ' meta',
    '8',
    'META',
    'Meta',
])
def test_get_meta_negative(endpoint):
    response = base_request.get(endpoint, expected_error=True)

    assert response.status_code == 404
    assert response.json() == {'message': "Couldn't find Brewery"}
