import requests


class TeslaAPIClient:
    def __init__(self, email, password):
        self.base_url = 'https://owner-api.teslamotors.com'
        self.api_prefix = '/api/1'
        self.session = requests.Session()
        self.session.auth = (email, password)

    def get_token(self):
        return self.session.post(self.base_url + '/oauth/token').json()


class TeslaAPIClientMock(TeslaAPIClient):
    def __init__(self):
        self.base_url = 'https://private-anon-f1c89d946-timdorr.apiary-mock.com'
        self.session = requests.Session()
        self.api_prefix = '/api/1'
