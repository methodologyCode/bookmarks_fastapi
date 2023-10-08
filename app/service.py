from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from utils import FailedRequestApi, logger


class InfoHelper:
    """
    Извлекает из страницы ее название, описание, иконку.
    """

    TITLE_TAG_PARAMS = (('title',),)
    FAVICON_TAG = (('link', {'rel': 'shortcut icon'}),)
    DESCRIPTION_TAG_PARAMS = (
        ('meta', {'name': 'description'}),
        ('meta', {'property': 'og:description'}),
    )

    def __init__(self, url):
        self.url = url
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html, features='html.parser')

    def get_html(self):
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                                    'Chrome/102.0.0.0 Safari/537.36'}

        try:
            response = requests.get(self.url, headers=user_agent)
        except requests.exceptions.RequestException as e:
            logger.critical(f'Ошибка при отправке запроса {e}')
            raise FailedRequestApi('Cервис не доступен!')

        if response.status_code != HTTPStatus.OK:
            logger.error(f'Статус код {response.status_code}')
            raise FailedRequestApi('Неожиданный статус код от сервера')

        return response.text

    def get_info(self):
        return {
            'url': self.url,
            'title': self.get_title(),
            'description': self.get_description(),
            'favicon': self.get_favicon(),
        }

    def get_tag(self, tag_params):
        """
        Метод для получения любого тэга по параметрам.
        """
        for params in tag_params:
            tag = self.soup.find(*params)
            if tag:
                return tag
        return None

    def get_title(self):
        """
        Получаем название страницы.
        """
        title_tag = self.get_tag(self.TITLE_TAG_PARAMS)
        if title_tag:
            return title_tag.text

        return 'Не удалось получить название'

    def get_description(self):
        """
        Получаем описание страницы.
        """
        description_tag = self.get_tag(self.DESCRIPTION_TAG_PARAMS)
        if description_tag:
            return description_tag.get('content')

        return 'Не удалось получить описание'

    def get_favicon(self):
        """
        Получаем favicon страницы.
        """
        favicon = self.get_tag(self.FAVICON_TAG)
        if favicon is None or not favicon.get('href'):
            return 'Не удалось получить иконку'

        return favicon.get('href')
