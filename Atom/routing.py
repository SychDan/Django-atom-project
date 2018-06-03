from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/post/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

"""""
channel_routing = {
    'websocket.connect': 'Atom.consumers.ws_connect',
    'websocket.receive': 'Atom.consumers.ws_message',
    'websocket.disconnect': 'Atom.consumers.ws_disconnect',
}
"""""