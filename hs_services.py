import requests
from requests.auth import HTTPBasicAuth


class HsService:
    def __init__(self, http_params):
        self.url = http_params['url']
        self.username = http_params['user']
        self.password = http_params['pass']
        self.android_id = http_params['android_id']
        self.device_model = http_params['device_model']
        self.user_name = http_params['user_name']

        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

    def send_data(self, data):
        answer = {'empty': True}
        if not data:
            return answer

        try:
            r = requests.post(f'{self.url}/simple_accounting/documents?android_id={self.android_id}',
                              auth=self.auth,
                              headers=self.headers,
                              params={'user_name': self.user_name, 'device_model': self.device_model},
                              data=data)

            answer['status_code'] = r.status_code
            if r.status_code == 200:
                answer['empty'] = False
            else:
                answer['empty'] = True
                answer['Error'] = r.text
        except Exception as e:
            answer['empty'] = True
            answer['Error'] = e.args[0]

        return answer
