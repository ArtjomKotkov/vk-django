from .bots_manager import CallBack
from .views import callback_signals
from django.dispatch import receiver


# user @receiver(callback_signals) to mark function, witch will be called on callback_api post method
# add #Callback.[event_type] for identificate event type which was called
# allowed event types:
# message_new
# message_reply
# message_edit
# message_allow
# message_deny
# keyboard_open(_id) - means that request contains payload with keyboard id which needs to send back
# define your answers here

@receiver(callback_signals)
def keyboard_opener(request, *args, **kwargs):
    """
    Default callback, when user press button, with payload which contains params { type = keyboard, id = int},
    change user keyboard to new keyboard, supports only saved keyboards.

    Don't delete this if you want to use modular keyboards.
    """
    CallBack.keyboard_open(request)

# Examples
@receiver(callback_signals)
@CallBack.message_new
def test(request, *args, **kwargs):
    print('Message_new called!')

@receiver(callback_signals)
@CallBack.button_press('test')
def keyboard_test(request, *args, **kwargs):
    print(f'Pressed button!')
