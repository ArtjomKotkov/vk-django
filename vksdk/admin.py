from django.contrib import admin
from .models import KeyBoards, Carousels
from django.utils.html import format_html
import json

class MyAdminSite(admin.AdminSite):
    site_header = 'VK-admin'


colors = {
    'primary': 'blue',
    'secondary': 'black',
    'negative': 'red',
    'positive': 'green'
}


class KeyboardModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'inline', 'one_time', 'keyboard_info')

    def keyboard_info(self, obj):
        rows = obj.keyboard.rows
        return_ = ''
        for row in range(0, len(rows)):
            str = f'<p><u>Row: {row} Buttons: {len(rows[row])}</u></p>'
            for button in rows[row]:
                if 'color' in button:
                    if 'payload' in button['action'] and button['action'].get('payload') != '':
                        payload = button['action'].get('payload')
                        if payload.get('type') == 'keyboard':
                            button["action"]["type"] = f'open keyboard ID: {payload.get("id")}'
                    str += f'<p style="color:{colors[button["color"]]}">Button type: {button["action"]["type"]}<p>'
                else:
                    str += f'<p>Button type: {button["action"]["type"]}<p>'
            return_ += str
        return format_html(return_)

    def inline(self, obj):
        return obj.keyboard.inline

    inline.short_description = 'Inline'
    inline.boolean = True

    def one_time(self, obj):
        return obj.keyboard.one_time

    one_time.short_description = 'One Time'
    one_time.boolean = True


admin_site = MyAdminSite(name='myadmin')
admin_site.register(KeyBoards, KeyboardModel)
admin_site.register(Carousels)
