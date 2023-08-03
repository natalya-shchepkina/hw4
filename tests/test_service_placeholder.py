import string

import pytest

import random

import config

import requests

from jsonschema import validate
from src.base_request import BaseRequest

url = config.BASE_URL_PLACEHOLDER
base_request = BaseRequest(url)


def test_json_schema():
    response = base_request.get('posts/1')

    schema = {
        "type": "object",
        "properties": {
            "body": {"type": "string"},
            "id": {"type": "number"},
            "title": {"type": "string"},
            "userId": {"type": "number"}
        },
        "required": ["body", "id", "title", "userId"]
    }
    assert response.status_code == 200
    validate(instance=response.json(), schema=schema)


@pytest.mark.parametrize('title, userId', [
    ('', '#'),
    (-1, 0),
    (0, 1000),
    (1000, -1),
    ('#', '')
])
def test_post_request(title, userId):
    body = {
        'title': title,
        'body': 'bar',
        'userId': userId
    }
    response = base_request.post('posts', body)

    assert response.json()['title'] == title
    assert response.json()['body'] == 'bar'
    assert response.json()['userId'] == userId


@pytest.fixture
def generate_random_string():
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for _ in range(random.randint(0, 100)))
    return rand_string


def test_patch_request(generate_random_string):
    body = {
        'title': generate_random_string,
        'body': generate_random_string,
        'userId': generate_random_string
    }
    response = requests.patch('https://jsonplaceholder.typicode.com/posts/1', body)

    assert response.json()['title'] == body['title']
    assert response.json()['body'] == body['body']
    assert response.json()['userId'] == body['userId']


@pytest.mark.parametrize('userId', [-1, 0, 11, ''])
def test_filtration_negative(userId):
    response = base_request.get('posts', params={'userId': userId})

    assert response.json() == []


def test_delete_request():
    body = {
        'title': '',
        'body': '',
        'userId': ''
    }
    resource_id = base_request.post('posts', body).json()['id']
    response = base_request.delete(f'posts/{resource_id}')

    assert response.status_code == 200
    assert response.json() == {}
