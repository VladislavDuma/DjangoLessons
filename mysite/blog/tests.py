# Необходимо для запуска тестов из PyCharm'a с дебагером
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
# ------------------------------------------------------

from django.test import TestCase

from blog.models import Post


class PostTestCase(TestCase):
    """
    setUpTestData используется при тестировании с терминала.
    Создаёт временную пустую БД. При тестировании с дебагером в PyCharm не требуется.

    P.S. В дебагере и терминале разное количество контекстов (71 и 4) и ошибка с индексами
    """

    @classmethod
    def setUpTestData(cls):
        cls.data = Post.objects.create(title='Realme 8i')

    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'], 'home')
        # self.assertEqual(response.context[3].dicts[3]['posts'][0].title, 'Realme 8i')
        self.assertEqual(response.context['posts'][0].title, 'Realme 8i')


class PostTestFixtureCase(TestCase):
    """
    Фикстуры используются при извлечении данных из дампа данных
    Пример выгрузки:
    >>> python manage.py dumpdata blog --indent 2 > fixtures/post_data.json
    """
    fixtures = ['fixtures/post_data.json']

    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.context['posts'][0].title, 'Realme 8i')
