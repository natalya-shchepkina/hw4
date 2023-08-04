import requests


class BaseRequest:

    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, params=None, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url, params=params)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200 \
                    or response.status_code == 201 and not expected_error:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        return response

    def get(self, endpoint, params=None, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'GET', params, expected_error=expected_error)
        return response

    def post(self, endpoint, body=None, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'POST', data=body, expected_error=expected_error)
        return response

    def delete(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'DELETE')
        return response



