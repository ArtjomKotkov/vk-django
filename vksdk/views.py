import json
import requests

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import View
from .bots_manager import CallBack
from django.dispatch import Signal, receiver
from django.http import HttpResponse

from .vk_settings import CALLBACK_GROUPID, CALLBACK_CODE

callback_signals = Signal(providing_args=['request'])


@method_decorator(csrf_exempt, name='dispatch')
class CallBackView(View):

    def post(self, request):
        """
        Take requests from VK callback api, and make signal (signals describe in callback_signals.py) to answer on it.
        """
        json_ = json.loads(request.body)

        # Connect to group, for validation
        if json_.get('type') == 'confirmation' and str(json_.get('group_id')) == CALLBACK_GROUPID:
            return HttpResponse(CALLBACK_CODE, status=200)

        # Send signal to answer on callback_api
        else:
            callback_signals.send_robust(sender=self.__class__, request=json.loads(request.body))
            return HttpResponse('ok', 200)


# Import callback_api methods
from .callback_signals import *

