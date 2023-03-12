import requests as re


class WikiManager:
    url = "https://en.wikipedia.org/w/api.php"

    def __init__(self, text):
        self.text = text

    def params(self):
        return {
            'action': 'opensearch',
            'search': self.text,
            'limit': 1,
            'namespace': 0,
            'format': 'json'
        }

    def get_result(self):
        response = re.get(
            url=self.url,
            params=self.params()
        )

        if response.status_code == 200:
            try:
                return response.json()[3][0]
            except Exception as e:
                print(e)
