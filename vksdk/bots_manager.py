import logging
import requests
import json
import random

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .vk_settings import *
from .models import KeyBoards, Carousels

# BUTTONS COLORS
BLUE = 'primary'  # blue
WHITE = 'secondary'  # white
RED = 'negative'  # red
GREEN = 'positive'  # green

# BUTTONS TYPES
TEXT = 'text'
OPEN_LINK = 'open_link'
LOCATION = 'location'
VK_PAY = 'vkpay'
VK_APPS = 'open_app'


class CallBack:
    """
    Vk callback api realization, include events decorators.
    Event's function are in callback_signals.py.
    """

    # MESSAGES EVENTS DECORATORS
    # CUSTOM EVENTS
    @staticmethod
    def button_press(name):
        """
        Callback will be called when payload contains name param, button with name was pressed.
        """

        def keyboard_inner(func):
            def wrapper(request, *args, **kwargs):
                if request.get('type') == 'message_new' and request['object'].get('payload').get('name') == name:
                    return func(request, *args, **kwargs)
                else:
                    return

            return wrapper

        return keyboard_inner

    @staticmethod
    def keyboard_open(request):
        """
        Callback will be called when payload contains type = keyboard, send new keyboard to user.
        """
        if request.get('type') == 'message_new' and request['object'].get('payload').get('type') == 'keyboard' and \
                request['object'].get('payload').get('id', None) is not None:
            user = request['object']['from_id']
            response = Message.send_keyboard(user_ids=[user], message='Меняем клавиатуру',
                                             keyboard=KeyBoard.load_keyboard(id=request['object']['payload']['id']))
            return response

    # STANDART EVENTS
    @staticmethod
    def message_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get('type') == 'message_new' and request['object'].get('payload').get(
                    'type') != 'None' and request['object'].get('payload').get('name', None) is None:
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def message_reply(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "message_reply":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def message_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "message_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def message_allow(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "message_allow":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def message_deny(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "message_deny":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def photo_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "photo_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def photo_comment_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "photo_comment_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def photo_comment_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "photo_comment_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def photo_comment_restore(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "photo_comment_restore":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def photo_comment_delete(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "photo_comment_delete":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def  # Audio(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "#Audio":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def audio_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "audio_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def video_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "video_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def video_comment_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "video_comment_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def video_comment_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "video_comment_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def video_comment_restore(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "video_comment_restore":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def video_comment_delete(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "video_comment_delete":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_post_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_post_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_repost(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_repost":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_reply_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_reply_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_reply_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_reply_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_reply_restore(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_reply_restore":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def wall_reply_delete(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "wall_reply_delete":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def board_post_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "board_post_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def board_post_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "board_post_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def board_post_restore(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "board_post_restore":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def board_post_delete(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "board_post_delete":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def market_comment_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "market_comment_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def market_comment_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "market_comment_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def market_comment_restore(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "market_comment_restore":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def market_comment_delete(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "market_comment_delete":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def group_leave(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "group_leave":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def group_join(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "group_join":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def user_block(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "user_block":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def user_unblock(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "user_unblock":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def poll_vote_new(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "poll_vote_new":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper

    @staticmethod
    def group_officers_edit(func):
        def wrapper(request, *args, **kwargs):
            if request.get("type") == "group_officers_edit":
                return func(request, *args, **kwargs)
            else:
                return

        return wrapper


class Message:

    @staticmethod
    def send(user_ids: list, message, attachment='', sticker_id=''):
        response = requests.get(
            f'https://api.vk.com/method/messages.send?user_ids={",".join(user_ids)}&'
            f'fields={",".join(user_ids)}&'
            f'message={message}&'
            f'random_id={random.randint(-9223372036854775808, 9223372036854775807)}&'
            f'attachment={attachment}&'
            f'sticker_id={sticker_id}&'
            f'access_token={AUTH_CLIENT.community_key}&'
            f'v=5.103')
        return response

    @staticmethod
    def send_photo(user_ids: list, photo):
        response = requests.get(
            f'https://api.vk.com/method/messages.send?user_ids={",".join(user_ids)}&'
            f'fields={",".join(user_ids)}&'
            f'random_id={random.randint(-9223372036854775808, 9223372036854775807)}&'
            f'attachment={photo}&'
            f'access_token={AUTH_CLIENT.community_key}&'
            f'v=5.103')
        return response

    @staticmethod
    def send_keyboard(user_ids: list, message: str, keyboard):
        response = requests.get(
            f'https://api.vk.com/method/messages.send?user_ids={",".join(user_ids)}&'
            f'fields={",".join(user_ids)}&'
            f'message={message}&'
            f'random_id={random.randint(-9223372036854775808, 9223372036854775807)}&'
            f'keyboard={keyboard}&'
            f'access_token={AUTH_CLIENT.community_key}&'
            f'v=5.103')
        return response

    @staticmethod
    def send_carousel(user_ids: list, message: str, carousel):
        response = requests.get(
            f'https://api.vk.com/method/messages.send?user_ids={",".join(user_ids)}&'
            f'fields={",".join(user_ids)}&'
            f'message={message}&'
            f'random_id={random.randint(-9223372036854775808, 9223372036854775807)}&'
            f'template={carousel}&'
            f'access_token={AUTH_CLIENT.community_key}&'
            f'v=5.103')
        return response


# DECORATOR
def check_buttons_count(func):
    def wrapper(self, *args, **kwargs):
        if sum(len(row) for row in self.rows) >= 40 and not self.inline:
            return logging.error('Not-inline button massive may contain 40 buttons')
        elif sum(len(row) for row in self.rows) >= 10 and self.inline:
            return logging.error('Not-inline button massive may contain 10 buttons')
        if len(self.rows[-1]) >= 5:
            return logging.error('Max button count in row is 10')
        func(self, *args, **kwargs)

    return wrapper


class KeyBoard:

    def __init__(self, one_time: bool, inline: bool, name=None):
        self.id = None
        self.name = name
        self.one_time = one_time
        self.inline = inline
        if self.inline and self.one_time:
            raise ValidationError('one_time field is not available for inline keyboard')
        self.json = dict(one_time=one_time,
                         inline=inline)
        self.rows = []

    def __repr__(self):
        keyboard_info = self.json
        keyboard_info.update(buttons=self.rows)
        return json.dumps(keyboard_info)

    def add_row(self):
        if not self.inline and len(self.rows) >= 10:
            return logging.error('Not-inline keyboard may contain only 10 rows')
        elif self.inline and len(self.rows) >= 6:
            return logging.error('Not-inline keyboard may contain only 6 rows')
        self.rows.append([])

    @check_buttons_count
    def add_button_text(self, label, payload: dict = None, color=None, name=None):
        button = dict(action=dict())
        if color:
            button.update(color=color)
        if payload:
            payload.update(name=name)
        button['action'].update(dict(type=TEXT, label=label, payload=KeyBoard.payload_serializer(payload)))
        self.rows[-1].append(button)

    @check_buttons_count
    def add_button_link(self, link, label, payload: dict = None, name=None):
        button = dict(action=dict())
        if payload:
            payload.update(name=name)
        button['action'].update(
            dict(type=OPEN_LINK, label=label, payload=KeyBoard.payload_serializer(payload), link=link))
        self.rows[-1].append(button)

    @check_buttons_count
    def add_button_location(self, payload: dict = None, name=None):
        button = dict(action=dict())
        if payload:
            payload.update(name=name)
        button['action'].update(dict(type=LOCATION, payload=KeyBoard.payload_serializer(payload)))
        self.rows[-1].append(button)

    @check_buttons_count
    def add_button_pay(self, hash, payload: dict = None, name=None):
        button = dict(action=dict())
        if payload:
            payload.update(name=name)
        button['action'].update(dict(type=VK_PAY, payload=KeyBoard.payload_serializer(payload), hash=hash))
        self.rows[-1].append(button)

    @check_buttons_count
    def add_button_app(self, app_id, owner_id, hash, payload: dict = None, name=None):
        button = dict(action=dict())
        if payload:
            payload.update(name=name)
        button['action'].update(dict(type=VK_APPS,
                                     payload=KeyBoard.payload_serializer(payload),
                                     app_id=app_id,
                                     owner_id=owner_id,
                                     hash=hash))
        self.rows[-1].append(button)

    @check_buttons_count
    def add_button_keyboard(self, label, keyboard_id: int, color, name=None):
        button = dict(action=dict())
        if color:
            button.update(color=color)
        button['action'].update(type=TEXT, label=label, payload=dict(type='keyboard', id=keyboard_id))
        button['action']['payload'].update(name=name)
        self.rows[-1].append(button)

    @staticmethod
    def payload_serializer(_dict):
        if not _dict:
            return ''
        return json.dumps(_dict)

    def save(self):
        if KeyBoards.objects.filter(name__exact=self.name).exists():
            raise ValidationError(f'Keyboard with name "{self.name}" already exist')
        keyboard = KeyBoards.objects.create(name=self.name, keyboard=self)
        self.id = keyboard.id
        return self.id

    @staticmethod
    def load_keyboard(id: int):
        try:
            object = KeyBoards.objects.get(pk=id)
            return object.keyboard
        except ObjectDoesNotExist:
            raise


def check_buttons_count_corousel(func):
    def wrapper(self, *args, **kwargs):
        if sum(len(row) for row in self.rows) >= 3 and not self.inline:
            return logging.error('Not-inline button massive may contain 40 buttons')
        func(self, *args, **kwargs)

    return wrapper


class Carousel:

    def __init__(self, name=None):
        self.name = name
        self.elements = []

    def __repr__(self):
        elements = [element.__repr__() for element in self.elements]
        repr_ = dict(
            type='carousel',
            elements=elements
        )
        return json.dumps(repr_)

    def add_element(self, title, description, photo_id, link=None):
        if len(self.elements) >= 10:
            raise ValidationError('Carousel can contain only 10 elements')
        element = self.CarouselElement(title, description, photo_id, link)
        self.elements.append(element)
        return element

    def add_exit_element(self, title, description, photo_id, keyboard, link=None):
        # first button - open keuboard
        if len(self.elements) >= 10:
            raise ValidationError('Carousel can contain only 10 elements')
        element = self.CarouselElement(title, description, photo_id, link)
        element.add_button_keyboard(keyboard_id=keyboard, color=GREEN, label='Open home keyboard')
        self.elements.append(element)
        return element

    @staticmethod
    def check_support(request):
        # call when new_message callback function is called
        if 'client_info' in request['object']:
            return request['object']['client_info']['carousel']
        else:
            return False

    @staticmethod
    def load_carousel(id: int):
        try:
            object = Carousels.objects.get(pk=id)
            return object.carousel
        except ObjectDoesNotExist:
            raise

    def save(self):
        if self.name is not None:
            return Carousels.objects.create(name=self.name, carousel=self)
        else:
            # добавить вызов ошибки
            pass

    class CarouselElement:
        def __init__(self, title, description, photo_id, link=None):
            self.title = title
            self.description = description
            self.photo_id = photo_id
            self.rows = []
            if link is not None:
                self.action = dict(typy='open_link', link=link)
            else:
                self.action = dict(type='open_photo')

        def __repr__(self):
            repr_ = dict(
                title=self.title,
                description=self.description,
                action=self.action,
                photo_id=self.photo_id,
                buttons=self.rows
            )
            return repr_

        @check_buttons_count_corousel
        def add_button_text(self, label, payload: dict = None, color=None, name=None):
            button = dict(action=dict())
            if color:
                button.update(color=color)
            if payload:
                payload.update(name=name)
            button['action'].update(dict(type=TEXT, label=label, payload=KeyBoard.payload_serializer(payload)))
            self.rows.append(button)

        @check_buttons_count_corousel
        def add_button_link(self, link, label, payload: dict = None, name=None):
            button = dict(action=dict())
            if payload:
                payload.update(name=name)
            button['action'].update(
                dict(type=OPEN_LINK, label=label, payload=KeyBoard.payload_serializer(payload), link=link))
            self.rows.append(button)

        @check_buttons_count_corousel
        def add_button_location(self, payload: dict = None, name=None):
            button = dict(action=dict())
            if payload:
                payload.update(name=name)
            button['action'].update(dict(type=LOCATION, payload=KeyBoard.payload_serializer(payload)))
            self.rows.append(button)

        @check_buttons_count_corousel
        def add_button_pay(self, hash, payload: dict = None, name=None):
            button = dict(action=dict())
            if payload:
                payload.update(name=name)
            button['action'].update(dict(type=VK_PAY, payload=KeyBoard.payload_serializer(payload), hash=hash))
            self.rows.append(button)

        @check_buttons_count_corousel
        def add_button_app(self, app_id, owner_id, hash, payload: dict = None, name=None):
            button = dict(action=dict())
            if payload:
                payload.update(name=name)
            button['action'].update(dict(type=VK_APPS,
                                         payload=KeyBoard.payload_serializer(payload),
                                         app_id=app_id,
                                         owner_id=owner_id,
                                         hash=hash))
            self.rows.append(button)

        @check_buttons_count_corousel
        def add_button_keyboard(self, label, keyboard_id: int, color, name=None):
            button = dict(action=dict())
            if color:
                button.update(color=color)
            button['action'].update(type=TEXT, label=label, payload=dict(type='keyboard', id=keyboard_id))
            button['action']['payload'].update(name=name)
            self.rows.append(button)


class Attachments:
    class Photos:

        @staticmethod
        def instance(id, access_token='', prefix=True):
            if prefix:
                str = f'photo{id}'
                if access_token != '':
                    str += f'_{access_token}'
            else:
                str = f'{id}'
                if access_token != '':
                    str += f'_{access_token}'
            return str

        @staticmethod
        def getMessagesUploadServer(peer_id=None):
            if peer_id is not None:
                peer_id = f'peer_id={peer_id}&'
            else:
                peer_id = ''
            response = requests.get(
                f'https://api.vk.com/method/photos.getMessagesUploadServer?'
                f'{peer_id}'
                f'access_token={AUTH_CLIENT.community_key}&'
                f'v=5.103')
            return response

        @staticmethod
        def upload_file(file, response):
            response = requests.post(response.json()['response']['upload_url'], files=dict(photo=open(file, 'rb')))
            return response

        @staticmethod
        def saveMessagesPhoto(response):
            dict = response.json()
            response2 = requests.get(
                f'https://api.vk.com/method/photos.saveMessagesPhoto?'
                f'photo={dict["photo"]}&'
                f'server={dict["server"]}&'
                f'hash={dict["hash"]}&'
                f'access_token={AUTH_CLIENT.community_key}&'
                f'v=5.103')
            return response2
