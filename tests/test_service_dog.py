import pytest
import config

from src.base_request import BaseRequest

url = config.BASE_URL_DOG
base_request = BaseRequest(url)


GET_ALL_SUB_BREEDS = 'breed/hound/list'
GET_IMAGE_ANY_BREED = 'breeds/image/random'


def test_get_all_sub_breed():
    response = base_request.get(GET_ALL_SUB_BREEDS)

    assert response.json().get('status') == 'success'
    assert isinstance(response.json().get('message'), list)


def test_get_image_any_breed():
    response = base_request.get(GET_IMAGE_ANY_BREED)

    assert response.json().get('status') == 'success'
    assert '.jpg' in response.json().get('message')


@pytest.mark.parametrize('quantity', [
    1,
    25,
    50
])
def test_get_images_any_breed(quantity):
    response = base_request.get(f'{GET_IMAGE_ANY_BREED}/{quantity}')

    assert response.json().get('status') == 'success'
    assert len(response.json().get('message')) == quantity


@pytest.mark.parametrize('quantity', [0, 51])
def test_get_images_any_breed_negative(quantity):
    response = base_request.get(f'{GET_IMAGE_ANY_BREED}/{quantity}')

    assert len(response.json().get('message')) != quantity


@pytest.mark.parametrize('breed', ['mix', 'akita', 'whippet'])
def test_get_image_breed(breed):
    response = base_request.get(f'breed/{breed}/images/random')

    assert response.json().get('status') == 'success'
    assert '.jpg' in response.json().get('message')
    assert breed in response.json().get('message')

