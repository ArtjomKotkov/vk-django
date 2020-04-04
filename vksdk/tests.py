from django.test import TestCase, Client
from .models import KeyBoards, Carousels
import vksdk.bots_manager as B
from django.urls import reverse_lazy
import json


class KeyBoardModelTest(TestCase):

    def setUp(self):
        keyboard = B.KeyBoard(one_time=False, inline=False, name='one')
        keyboard.add_row()
        keyboard.add_button_text(label='Получить задачи на ближайшие 3 дня', color=B.BLUE)
        keyboard.save()

    def test_model2(self):
        key = KeyBoards.objects.all().first()
        self.assertEqual(key.keyboard.name, 'one')


class CarouselsModelTest(TestCase):
    def setUp(self):
        carousel = B.Carousel(name='one')
        elem1 = carousel.add_element(title='test title', description='test description', photo_id='test photo')
        elem1.add_button_text(label='button 1 elem 1')
        elem1.add_button_text(label='button 2 elem 1')
        elem2 = carousel.add_element(title='test title2', description='test description2', photo_id='test photo2')
        carousel.save()

    def test_carousels(self):
        q = Carousels.objects.all().first()
        self.assertEqual(q.name, 'one')

    def test_loadcarousel(self):
        q = B.Carousel.load_carousel(1)
        self.assertEqual(q.name, 'one')



class CallBackApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        keyboard = B.KeyBoard(one_time=False, inline=False, name='one')
        keyboard.add_row()
        keyboard.add_button_text(label='Получить задачи на ближайшие 3 дня', color=B.BLUE)
        keyboard.save()

    def test_signals(self):
        data = {
            "type": "message_new",
            "object": {
                'payload': 'None'
            },
            "group_id": 1,
            "secret": "sjr948dff3kjnfd3"
        }
        response = self.client.post(reverse_lazy('callback_url'), json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_open_keyboard(self):
        data = {
            "type": "message_new",
            "object": {
                'from_id': '41407234',
                'payload': dict(type='keyboard', id=1)
            },
            "group_id": 1,
            "secret": "sjr948dff3kjnfd3"
        }
        response = self.client.post(reverse_lazy('callback_url'), json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_button_press(self):
        data = {
            "type": "message_new",
            "object": {
                'payload': dict(name='test')
            },
            "group_id": 1,
            "secret": "sjr948dff3kjnfd3"
        }
        response = self.client.post(reverse_lazy('callback_url'), json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
