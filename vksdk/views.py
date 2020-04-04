from django.views.generic import View
from .bots_manager import CallBack
from django.dispatch import Signal, receiver
from django.http import HttpResponse
import json

callback_signals = Signal(providing_args=['request'])


class CallBackView(View):
    def post(self, request):
        # Check host server and send response with code
        CallBack.session_check(request)
        # Send signal to answer on callback_api
        callback_signals.send_robust(sender=self.__class__, request=json.loads(request.body))
        return HttpResponse('', 200)

# import callback_api methods
import vksdk.callback_signals
